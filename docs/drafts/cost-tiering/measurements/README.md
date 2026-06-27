# Token-spend measurements

A lightweight, real-data log for the cost-tiering work. We are about to change how
many artifacts and reviews each kind of work produces; this records what each test
project actually costs so the design is tuned on measured spend, not estimates.

This is a draft instrument that can be used **now**, before any behavior change, to
baseline the current (flat) pipeline. Re-measure after each change to see the delta.

## Ground truth

Claude Code writes a per-session transcript at
`~/.claude/projects/<project-slug>/<session-id>.jsonl`. Each assistant turn carries
a `usage` block with the real numbers: `input_tokens`, `cache_creation_input_tokens`,
`cache_read_input_tokens`, `output_tokens`. Sub-agent work may live in sibling
`agent-*.jsonl` files — include them for a full project total.

**Codex** writes per-session rollout transcripts at
`~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`. Each turn logs a cumulative
`total_token_usage` (input incl. cached / `cached_input_tokens` / output /
`reasoning_output_tokens`); the last one is the session total. Codex runs each
sub-agent as its **own** rollout, so a project's reviews are separate files — pass
them too for a full project total. Mapping into this log: `cr` = cached_input,
`cc` = 0 (OpenAI has no separate cache-write charge), `out` = output + reasoning,
`in` = input − cached.

`token-report.py` auto-detects the format, parses one or more transcripts, and totals
the four numbers. They are ground truth. It also prints an **input-equivalent** figure
that collapses them into one comparable unit using each tool's billing ratios
(Claude: cache write 1.25×, cache read 0.1×, output 5×; Codex/GPT-5 family: cache read
0.1×, output 8×). Adjust `WEIGHTS` in the script if pricing changes.

## Procedure (per test project)

1. Run one project end to end in its own session (ideally one project per session,
   so the transcript maps cleanly to one run).
2. Find the session transcript and run:
   ```
   python3 token-report.py ~/.claude/projects/<slug>/<session-id>.jsonl
   # or, with sub-agents:
   python3 token-report.py ~/.claude/projects/<slug>/<session-id>*.jsonl
   # or by id:
   python3 token-report.py --session <session-id>
   ```
3. Copy the printed `log line`, fill in the project metadata fields, and append it to
   `token-log.jsonl`.

## Record fields (`token-log.jsonl`, one JSON object per line)

- `date` — run date.
- `tool` — `claude` | `codex`.
- `model` — model id (e.g. `gpt-5.5`, `claude-opus-4-8`).
- `medium` — `text` | `image` | `audio` | `video`.
- `scale_level` — `compact_artifact` | `structured_single_artifact` | `cumulative_work` | `full_long_form_project`.
- `output_kind` — free text, e.g. "sub-1-min social video".
- `subagents` — count of review/worker sub-agents spawned.
- `notes` — anything notable (e.g. "loaded full video stack", "express path", "after review-gating change").
- `turns` — assistant turns in the run.
- `in`, `cc`, `cr`, `out` — raw input / cache-creation / cache-read / output tokens.
- `input_equiv` — weighted single-number cost (see Ground truth).

## How to read the four numbers

- `cr` (cache read) high → lots of context re-read every turn. Lower it with fewer/
  smaller loaded docs (index-first reference loading) and fewer turns (single-shot).
- `cc` (cache creation) high → context churns / grows as new material loads each turn.
  Lower it by loading less up front and not re-expanding the working set.
- `out` high → producing large records. Lower it with record collapse (compact tiers)
  and concise output style.
- `in` is usually tiny once caching is warm.

## Per-turn curve (for measuring improvements)

`token-curve.py <transcript.jsonl> [out.html] [--title T]` writes a self-contained HTML
chart of per-turn context size + cumulative tokens for a run (Claude or Codex, auto-detected;
Chart.js is pinned with Subresource Integrity). Use it to see *where* context balloons and to
compare before/after a change:

```
python3 token-curve.py ~/.codex/sessions/2026/06/27/rollout-...jsonl out.html --title "express-path test"
```

Baselines live in `curves/`. `curves/queen-bee-2026-06-26.html` is the pre-change reference:
244 turns, peak 236k, mean 126k context/turn, 30.7M total — cost ≈ turns × mean-context. After
the express-path / reset changes land, generate the new run's curve into `curves/` and the area
under the red line should drop sharply.

## Goal

After ~5 runs across cells (especially video/compact and a long-form journey), the
log should show where spend concentrates per cell and validate or correct the design's
estimated cost weights. Use it to pick the highest-leverage change to implement first.
