#!/usr/bin/env python3
"""Faithful routing eval for the public Artist OS skill surface.

Unlike the meta-prompt approach (which asks the model "which would you pick?"
and is dominated by framing), this mirrors the skill-creator's validated method:
install all skills as real available skills, fire the RAW user query with no
framing, and detect which skill Claude actually consults first.

The current Artist OS bundle intentionally exposes one public skill (`artist-os`)
plus internal mode files, so the signed-off label set is binary: `artist-os` or
`none`. The harness still reads the on-disk skill set so it can catch future
routing-surface changes without being rewritten.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import select
import shutil
import subprocess
import time
import uuid
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO / "skills"


def load_skills() -> dict[str, dict]:
    """key -> {name, description}. `name` is the real frontmatter name."""
    out: dict[str, dict] = {}
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        key = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8")
        name = re.search(r"^name:\s*(.+?)\s*$", text, re.MULTILINE)
        desc = re.search(r"^description:\s*(.+?)\s*$", text, re.MULTILINE)
        if name and desc:
            out[key] = {"name": name.group(1).strip(), "desc": desc.group(1).strip()}
    return out


def setup_project(skills: dict[str, dict], root: Path) -> dict[str, str]:
    """Install all skills as command files. Return {real_name: key}."""
    cmd_dir = root / ".claude" / "commands"
    if cmd_dir.exists():
        shutil.rmtree(root / ".claude")
    cmd_dir.mkdir(parents=True, exist_ok=True)
    name_to_key: dict[str, str] = {}
    for key, s in skills.items():
        name = s["name"]
        indented = "\n  ".join(s["desc"].split("\n"))
        content = (f"---\ndescription: |\n  {indented}\n---\n\n"
                   f"# {name}\n\nThis skill handles: {s['desc']}\n")
        (cmd_dir / f"{name}.md").write_text(content)
        name_to_key[name] = key
    return name_to_key


def match_name(text: str, names: list[str]) -> str | None:
    """Return the LONGEST installed name appearing in text.

    Longest-match stays correct if future public skill names share prefixes.
    """
    hits = [n for n in names if n in text]
    return max(hits, key=len) if hits else None


def route_one(query: str, name_to_key: dict[str, str], project_root: str,
              model: str, timeout: int) -> str:
    """Run a raw query; return the key of the first consulted skill, or 'none'."""
    names = list(name_to_key)
    cmd = ["claude", "-p", query, "--output-format", "stream-json",
           "--verbose", "--include-partial-messages", "--model", model]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            cwd=project_root, env=env)
    buffer = ""
    pending = None
    acc = ""
    start = time.time()
    try:
        while time.time() - start < timeout:
            if proc.poll() is not None:
                rem = proc.stdout.read()
                if rem:
                    buffer += rem.decode("utf-8", errors="replace")
                # drain remaining lines below, then stop
            ready, _, _ = select.select([proc.stdout], [], [], 1.0)
            if not ready and proc.poll() is None:
                continue
            if proc.poll() is None:
                chunk = os.read(proc.stdout.fileno(), 8192)
                if chunk:
                    buffer += chunk.decode("utf-8", errors="replace")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "stream_event":
                    se = event.get("event", {})
                    t = se.get("type", "")
                    if t == "content_block_start":
                        cb = se.get("content_block", {})
                        if cb.get("type") == "tool_use":
                            if cb.get("name", "") in ("Skill", "Read"):
                                pending, acc = cb.get("name"), ""
                            else:
                                return "none"  # first action wasn't a skill consult
                    elif t == "content_block_delta" and pending:
                        d = se.get("delta", {})
                        if d.get("type") == "input_json_delta":
                            acc += d.get("partial_json", "")
                            m = match_name(acc, names)
                            if m:
                                return name_to_key[m]
                    elif t in ("content_block_stop", "message_stop"):
                        if pending:
                            m = match_name(acc, names)
                            return name_to_key[m] if m else "none"
                        if t == "message_stop":
                            return "none"
                elif event.get("type") == "assistant":
                    for ci in event.get("message", {}).get("content", []):
                        if ci.get("type") != "tool_use":
                            continue
                        if ci.get("name") in ("Skill", "Read"):
                            blob = json.dumps(ci.get("input", {}))
                            m = match_name(blob, names)
                            if m:
                                return name_to_key[m]
                        return "none"
                elif event.get("type") == "result":
                    return "none"
            if proc.poll() is not None and "\n" not in buffer:
                break
        return "none"
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evals", default=str(Path(__file__).parent / "routing-evals.json"))
    ap.add_argument("--model", default="opus")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--out", default=str(Path(__file__).parent / "out"))
    args = ap.parse_args()

    skills = load_skills()
    proj = Path(args.out) / "faithful-project"
    proj.mkdir(parents=True, exist_ok=True)
    name_to_key = setup_project(skills, proj)
    data = json.loads(Path(args.evals).read_text(encoding="utf-8"))
    evals = data["evals"]
    print(f"{len(skills)} skills installed, {len(evals)} queries x {args.runs} runs "
          f"(model={args.model})", flush=True)

    jobs = [(e, r) for e in evals for r in range(args.runs)]
    preds: dict[int, list[str]] = defaultdict(list)
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(route_one, e["query"], name_to_key, str(proj),
                          args.model, args.timeout): e for (e, _r) in jobs}
        for fut in as_completed(futs):
            e = futs[fut]
            try:
                preds[e["id"]].append(fut.result())
            except Exception as ex_:
                preds[e["id"]].append(f"__err__:{ex_}")
            done += 1
            print(f"  {done}/{len(jobs)}", flush=True)

    rows = []
    for e in evals:
        votes = Counter(preds[e["id"]])
        winner = votes.most_common(1)[0][0]
        rows.append({"id": e["id"], "query": e["query"], "target": e["target"],
                     "probe": e.get("probe", False), "predicted": winner,
                     "votes": dict(votes), "correct": winner == e["target"]})

    labels = list(skills) + ["none"]
    per = {}
    for lab in labels:
        tp = sum(1 for r in rows if r["target"] == lab and r["predicted"] == lab)
        fp = sum(1 for r in rows if r["target"] != lab and r["predicted"] == lab)
        fn = sum(1 for r in rows if r["target"] == lab and r["predicted"] != lab)
        per[lab] = {"prec": tp/(tp+fp) if tp+fp else None,
                    "rec": tp/(tp+fn) if tp+fn else None,
                    "fp": fp, "fn": fn, "support": sum(1 for r in rows if r["target"] == lab)}

    total = len(rows); correct = sum(r["correct"] for r in rows)
    probes = [r for r in rows if r["probe"]]; pc = sum(r["correct"] for r in probes)
    result = {"method": "faithful_available_skills", "model": args.model,
              "runs": args.runs, "overall_accuracy": correct/total,
              "correct": correct, "total": total,
              "probe_accuracy": pc/len(probes) if probes else None,
              "rows": rows, "per_skill": per}
    (Path(args.out) / "routing-results.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8")

    def p(x): return "  - " if x is None else f"{x*100:4.0f}%"
    md = [f"# Routing eval (real available_skills) — {args.model}, {args.runs} runs\n",
          f"**Overall: {correct}/{total} = {correct/total*100:.0f}%**  ",
          f"Probe accuracy: {pc}/{len(probes)} = {pc/len(probes)*100:.0f}%\n",
          "## Per-skill precision / recall\n",
          "| skill | support | precision | recall | fp | fn |",
          "|---|---|---|---|---|---|"]
    for lab in labels:
        s = per[lab]
        md.append(f"| {lab} | {s['support']} | {p(s['prec'])} | {p(s['rec'])} | {s['fp']} | {s['fn']} |")
    md += ["\n## Mis-routes\n", "| # | query | target | predicted | votes | probe |",
           "|---|---|---|---|---|---|"]
    for r in rows:
        if not r["correct"]:
            v = ", ".join(f"{k}:{n}" for k, n in r["votes"].items())
            md.append(f"| {r['id']} | {r['query'][:55]}… | {r['target']} | **{r['predicted']}** | {v} | {'★' if r['probe'] else ''} |")
    md += ["\n## All\n", "| # | target | predicted | ok | votes |", "|---|---|---|---|---|"]
    for r in rows:
        v = ", ".join(f"{k}:{n}" for k, n in r["votes"].items())
        md.append(f"| {r['id']} | {r['target']} | {r['predicted']} | {'✓' if r['correct'] else '✗'} | {v} |")
    (Path(args.out) / "routing-report.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\noverall {correct}/{total} = {correct/total*100:.0f}%, probes {pc}/{len(probes)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
