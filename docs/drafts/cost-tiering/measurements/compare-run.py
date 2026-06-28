#!/usr/bin/env python3
"""Compare a fresh Artist OS run against the logged FLAT baseline and check it
actually took the lean path.

Use after re-running a short-form video through the updated skill (lean
micro-journey recipe + Schema Load Economy) to measure the win against the
2026-06-27 Sage Wells flat baseline in token-log.jsonl.

Usage:
  compare-run.py <rollout.jsonl> [--label "lean rerun"]
  compare-run.py --session <id>  [--label "lean rerun"]

It prints three things:
  1. cost (raw four numbers + input-equivalent) — computed by reusing
     token-report.py's parser verbatim, so the numbers match the logged rows,
  2. per-turn context distribution vs the ~90k design cap,
  3. lean-path signals — did it load the recipe, AVOID the full video stack, and
     set micro_journey depth? — so a silent flat run can't masquerade as a win.
Then it shows the logged flat Sage Wells baseline for side-by-side reading.
"""
import json, os, sys, glob, importlib.util

CAP = 90_000
SESS_ROOTS = [
    os.path.expanduser("~/.codex/sessions"),
    os.path.expanduser("~/.codex/archived_sessions"),
]
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "token-log.jsonl")


def _load_token_report():
    """Import token-report.py (hyphenated name) so cost math is identical."""
    spec = importlib.util.spec_from_file_location("token_report", os.path.join(HERE, "token-report.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


TR = _load_token_report()


def resolve(arg, is_session):
    if not is_session:
        return arg
    for root in SESS_ROOTS:
        hits = glob.glob(os.path.join(root, "**", f"*{arg}*.jsonl"), recursive=True)
        if hits:
            return sorted(hits)[-1]
    sys.exit(f"no rollout found for session id {arg!r} under {SESS_ROOTS}")


def ctx_series(path):
    """Per-turn context, using token-report.py's exact turn definition (one entry
    per object carrying a structured total_token_usage)."""
    out = []
    for raw in open(path, encoding="utf-8", errors="ignore").read().splitlines():
        if not raw.strip():
            continue
        try:
            o = json.loads(raw)
        except Exception:
            continue
        if TR._find_last(o, "total_token_usage") is None:
            continue
        last = TR._find_last(o, "last_token_usage") or {}
        out.append(last.get("input_tokens", 0))
    return out


def signals(path):
    keys = {
        "recipe": "video-micro-journey-recipe",
        "video_journey": "video-journey.md",
        "storyboard_builder": "storyboard-prompt-builder",
        "micro_journey": "micro_journey",
        "schema_reads": ".schema.json",
    }
    counts = {k: 0 for k in keys}
    for line in open(path, encoding="utf-8", errors="ignore"):
        for k, s in keys.items():
            if s in line:
                counts[k] += line.count(s)
    return counts


def baseline():
    rows = []
    if os.path.exists(LOG):
        for line in open(LOG, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if "Sage Wells" in r.get("output_kind", ""):
                rows.append(r)
    return rows


def k(v):
    return f"{v/1000:.0f}k" if v < 1e6 else f"{v/1e6:.1f}M"


def main(argv):
    rest = [a for a in argv[1:] if not a.startswith("--")]
    is_session = "--session" in argv
    label = argv[argv.index("--label") + 1] if "--label" in argv else "this run"
    if not rest:
        print(__doc__); return 1
    path = resolve(rest[0], is_session)

    tool, d, turns = TR.parse_file(path)
    if turns == 0:
        sys.exit(f"no usage parsed from {path}")
    w = TR.WEIGHTS[tool]
    ieq = round(sum(d[c] * w[c] for c in d))

    ctx = ctx_series(path)
    n = len(ctx) or 1
    mean, peak, area = sum(ctx) // n, (max(ctx) if ctx else 0), sum(ctx)
    lo = sum(1 for x in ctx if x < 50_000)
    mid = sum(1 for x in ctx if 50_000 <= x < CAP)
    hi = sum(1 for x in ctx if x >= CAP)
    sig = signals(path)

    print(f"\n=== {label} ===  ({tool})\n{os.path.basename(path)}\n")
    print("cost:")
    print(f"  turns {turns}   in {d['in']:,}   cache-read {d['cr']:,}   out {d['out']:,}")
    print(f"  input-equivalent: {ieq:,}  ({k(ieq)})")
    print(f"\nper-turn context: mean {k(mean)}  peak {k(peak)}  area {area/1e6:.1f}M")
    print(f"  <50k: {lo} ({100*lo//n}%)   50-90k: {mid} ({100*mid//n}%)   >90k cap: {hi} ({100*hi//n}%)")

    def mark(ok):
        return "PASS" if ok else "WARN"
    print("\nlean-path signals:")
    print(f"  [{mark(sig['recipe']>0)}] loaded micro-journey recipe   (hits: {sig['recipe']})")
    print(f"  [{mark(sig['video_journey']==0 and sig['storyboard_builder']==0)}] avoided full video stack       "
          f"(video-journey: {sig['video_journey']}, storyboard-builder: {sig['storyboard_builder']})")
    print(f"  [{mark(sig['micro_journey']>0)}] set micro_journey depth        (hits: {sig['micro_journey']})")
    print(f"  [info] schema (.schema.json) references: {sig['schema_reads']}  "
          f"(lower + later = better — Schema Load Economy expects a small late cluster)")

    base = baseline()
    if base:
        bt = sum(r["turns"] for r in base)
        beq = sum(r["input_equiv"] for r in base)
        bmean = sum(r["cr"] for r in base) // bt
        print(f"\nflat Sage Wells baseline (token-log.jsonl, {len(base)} sessions, FLAT, split):")
        print(f"  turns {bt}   input-equiv {beq:,} ({k(beq)})   mean ctx/turn ~{k(bmean)}")
        dlt = mean - bmean
        print(f"\ndelta (mean ctx/turn — the cleanest apples-to-apples metric):")
        print(f"  {label}: {k(mean)}  vs  baseline ~{k(bmean)}  ->  {'-' if dlt<0 else '+'}{k(abs(dlt))} "
              f"({100*dlt//bmean:+d}%)")
        print("  (input-equiv here is one session vs a 3-session journey in the baseline — compare per-stage.)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
