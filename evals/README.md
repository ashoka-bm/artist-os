# Artist OS evals

Two regression guards for the skill family. They are **not** unit tests — they
call `claude -p` (cost tokens, need auth, take minutes), so run them by hand
before/after changing skill descriptions or the conductor, not in CI.

| eval | guards | when to run |
|---|---|---|
| `routing/` | skill **descriptions** (which skill triggers) | after editing any `description:` frontmatter |
| `conductor-behavior/` | the **conductor body** (phase order, gates, delegation, medium quirks) | after editing `skills/artist-os/SKILL.md` |

Prerequisites: the `claude` CLI on `PATH` and `python3` (stdlib only).

---

## routing/ — multi-class routing eval

For each labeled query in `routing-evals.json`, it installs all skills as real
available skills, fires the **raw** query through `claude -p` (no meta-framing),
and detects which skill Claude actually consults first. Produces a confusion
matrix + per-skill precision/recall.

```bash
python3 evals/routing/routing_eval.py --runs 5
# writes evals/routing/out/routing-report.md and routing-results.json
```

Read precision/recall as the two failure modes: low **precision** = a skill is
*greedy* (stealing siblings' prompts); low **recall** = a skill is *starved*. A
greedy skill and a starved skill are usually the same collision seen from both
sides, so tune the competing descriptions **together** and re-run the whole set.

**Why "raw query + real available_skills" and not "ask the model which to pick":**
an abstract "which skill should handle this?" prompt is dominated by its own
phrasing — we measured 62% / heavy-trigger / 42% on the *same* data just by
rewording the question. The only trustworthy framing is the one that mirrors
production: install the skills, send the bare user message, observe what Claude
consults. Keep a few queries whose answer is certain (e.g. an obvious full
transformation, an off-domain negative) as an instrument check — if one of those
flips, distrust the harness before the skill.

`routing-evals.json` is the signed-off label set. `probe: true` marks the
deliberately-hard cases (sibling collisions, cold-vs-records boundaries); they
encode routing *policy*, so re-confirm the labels if the policy changes.

---

## conductor-behavior/ — conductor behavior traces

The conductor is interactive and references many files, so this eval is run via
subagents producing a structured **trace** (phases, gates, delegations) that is
graded against a checklist. `eval-spec.md` has the test prompts, the per-prompt
subagent instructions, and the checklist. Procedure:

1. Snapshot the current conductor: `cp skills/artist-os/SKILL.md evals/conductor-behavior/baseline-SKILL.md`.
2. Spawn one subagent per test prompt (see `eval-spec.md`); save traces to `baseline/T1.md`, `T2.md`, etc.
3. Grade each trace against the checklist — this is the behavior to preserve.
4. Make the conductor change, then re-run the same prompts into `trimmed/`.
5. Diff: every checklist assertion that passed at baseline must still pass. A
   flipped assertion is real information loss, not a style change.

The baseline traces double as the spec: if a subagent can reconstruct the exact
behavior from the SKILL.md, the prose communicates it; the edit's job is to keep
those traces identical.

## disposable rehearsal artifacts

End-to-end rehearsal artifacts may live under `.tmp/` when the goal is evidence
for evals rather than resumable Artist OS project state. This is an eval-only
exception to the normal Workspace Library persistence contract: `.tmp/` records
can prove behavior and reveal contract gaps, but they are not durable project
state and should not be promoted wholesale. Promote only reduced fixtures,
tests, or docs that protect a specific finding.
