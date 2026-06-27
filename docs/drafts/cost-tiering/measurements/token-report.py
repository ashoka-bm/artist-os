#!/usr/bin/env python3
"""Summarize real token usage from a Claude Code or Codex session transcript.

Raw usage from the transcript is ground truth. The "input-equivalent" figure
collapses the components into one comparable unit using each tool's billing
ratios (adjust WEIGHTS if pricing changes).

Format is auto-detected:
- Claude Code: `~/.claude/projects/<slug>/<session-id>.jsonl`; per-turn
  `message.usage` (input / cache_creation / cache_read / output) is summed.
- Codex: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`; the last cumulative
  `total_token_usage` (input incl. cached / cached_input / output / reasoning)
  is used. Codex runs each sub-agent as its own rollout — pass those files too
  for a full project total.

Usage:
  token-report.py <transcript.jsonl> [more.jsonl ...]
"""
import json, sys, glob

WEIGHTS = {
    "claude": {"in": 1.0, "cc": 1.25, "cr": 0.1, "out": 5.0},
    "codex":  {"in": 1.0, "cc": 0.0,  "cr": 0.1, "out": 8.0},
}


def _find_last(obj, key):
    found = [None]
    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get(key), dict):
                found[0] = o[key]
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return found[0]


def parse_file(path):
    """Return (tool, {in,cc,cr,out}, turns)."""
    lines = [l for l in open(path, encoding="utf-8", errors="ignore").read().splitlines() if l.strip()]
    objs = []
    for l in lines:
        try:
            objs.append(json.loads(l))
        except Exception:
            pass
    is_codex = any('"total_token_usage"' in l for l in lines)
    d = {"in": 0, "cc": 0, "cr": 0, "out": 0}
    turns = 0
    if is_codex:
        last = None
        for o in objs:
            u = _find_last(o, "total_token_usage")
            if u:
                last, _ = u, turns
                turns += 1
        if last:
            cin = last.get("cached_input_tokens", 0)
            d["cr"] = cin
            d["in"] = last.get("input_tokens", 0) - cin
            d["out"] = last.get("output_tokens", 0) + last.get("reasoning_output_tokens", 0)
        return "codex", d, turns
    # claude: sum per-turn usage
    for o in objs:
        u = None
        if isinstance(o, dict):
            m = o.get("message")
            if isinstance(m, dict) and isinstance(m.get("usage"), dict):
                u = m["usage"]
            elif isinstance(o.get("usage"), dict):
                u = o["usage"]
        if u and "output_tokens" in u:
            turns += 1
            d["in"] += u.get("input_tokens", 0)
            d["cc"] += u.get("cache_creation_input_tokens", 0)
            d["cr"] += u.get("cache_read_input_tokens", 0)
            d["out"] += u.get("output_tokens", 0)
    return "claude", d, turns


def main(argv):
    files = []
    for a in argv[1:]:
        files += glob.glob(a)
    if not files:
        print("no transcript files found", file=sys.stderr)
        return 1
    agg = {"in": 0, "cc": 0, "cr": 0, "out": 0}
    turns = 0
    ieq = 0.0
    tools = set()
    for fp in files:
        tool, d, t = parse_file(fp)
        tools.add(tool)
        w = WEIGHTS[tool]
        for k in agg:
            agg[k] += d[k]
        ieq += sum(d[k] * w[k] for k in d)
        turns += t
    print(f"files: {len(files)}   tool(s): {','.join(sorted(tools))}   turns: {turns}")
    print(f"  fresh input:            {agg['in']:>13,}")
    print(f"  cache creation:         {agg['cc']:>13,}")
    print(f"  cache read (re-read):   {agg['cr']:>13,}")
    print(f"  output (+reasoning):    {agg['out']:>13,}")
    print(f"  raw total:              {sum(agg.values()):>13,}")
    print(f"  input-equivalent units: {round(ieq):>12,}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
