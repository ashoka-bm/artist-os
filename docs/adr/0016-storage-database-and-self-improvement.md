# Storage, Database, and Self-Improvement Finalization

Status: proposed. This is the finalized design; execution has not started. It is
written for review before any code changes.

Artist OS keeps durable state as JSON/JSONL files on disk (`project.json`
manifests, `events.jsonl`, `feedback-log.jsonl`, schema-backed `learning` and
`performance-signal` records, sidecars) and indexes them into a local SQLite
cache (`artist-os.sqlite`) so agents can quickly answer "what projects exist,
where do I resume, what was learned." The files are the source of truth; SQLite
is a disposable, rebuildable projection. That separation is correct and is not
being changed.

Three things are true today that keep the system from being "locked in":

1. **Sync is not fault-isolated.** Every write ends in a full-library
   `sync_db(args)` that indexes all manifests in one transaction, so one corrupt
   `project.json` aborts the index write for unrelated projects. Because the
   durable JSON write already committed, the file succeeds while the index
   silently does not.
2. **The self-improvement loop has no trigger.** The storage destinations exist
   and are schema-backed and tested (`add-feedback`, `add-learning`,
   `add-performance-signal`, `learnings-report`, `pending-learning-reviews`), but
   `skills/artist-os/SKILL.md` never calls them. Learning Review is described as
   something that "may" run, not something the conductor does. The mechanism
   exists with no invocation.
3. **The read path trusts the index absolutely.** The verbs that would surface
   learnings read SQLite only, with no fallback to files and no staleness signal.
   If any write's index leg fails, the conductor surfaces nothing while the files
   are correct — the loop can lie by omission.

This ADR finalizes all three at once, because they are one problem: **learning
writes ride on `sync`.** The self-improvement loop cannot be trusted until the
database underneath it is fault-isolated, scoped, non-destructive, and
self-healing at read time.

## Lineage and scope

The self-improvement pattern was proven first in an Agentic OS reference and
ported into InfluencerOS (whose own self-learning ADR is, coincidentally, also
numbered 0016 — a different repo). In both, the loop is two model-invoked skills
(`wrap-up` + `memory-write`) writing markdown `learnings.md` / `MEMORY.md`, plus
a `## Rules` / `## Self-Update` convention on behavior-changing skills. No hooks,
no cron, no vector store — those layer on later without redesign.

Artist OS is deliberately kept lighter than those systems. It is already ahead
on one axis: its learning is **structured schema-backed records**, not markdown.
So Artist OS keeps its superior store and borrows only the missing loop
mechanism — the trigger — not the elaborate infrastructure. InfluencerOS also
uses the same files-as-truth + SQLite-projection architecture, so its proven
sync patterns (per-scope delete/reinsert, per-source hash) are ported rather
than reinvented.

## Decision

Finalize Artist OS's storage, database, and self-improvement as one integrated
unit built on these invariants:

- **Files are truth; SQLite is a disposable projection.** No learning or
  feedback content is ever written to SQLite as its home. All self-improvement
  writes go through the existing CLI into structured records and `events.jsonl`.
- **Every write is scoped and fault-isolated.** A write to one project reaches
  the index even when another project's manifest is corrupt.
- **Reads reflect files.** The read step that surfaces learnings self-heals
  against the files it is about to trust, so a write that reached JSON but not
  the index cannot cause a silent miss.
- **The self-improvement loop is model-invoked, not automated.** The conductor
  triggers it by description. Hooks and cron remain deferred.
- **Promotion into the conductor is human-gated and presented plainly.** Nothing
  edits the eval-locked conductor file silently.

## The self-improvement loop

Three conductor behaviors and one new read verb. No new skills, no new markdown
memory files.

### Learning-Review-at-Start

At project start the conductor surfaces relevant prior learnings and applies
them. Before reading, it runs a scoped sync of the projects it is about to
surface (see "Read-path self-healing"), then reads their learning rules. Per the
existing policy in `docs/storage.md`: relevant Hard Learning applies by default
unless it conflicts with current Artist Meaning or approved plans; relevant Soft
Learning applies by default with brief disclosure. This policy is already
decided and is not reopened here.

### Session-start open-project triage

On a new session the conductor reviews open projects (status not complete,
archived, or missing) using the minimal `status` verb, and for each asks whether
it is still active or should be wrapped up. "Still going" resumes from
`resume_state`; "wrap it up" runs Close-Out. This prevents projects from
lingering in an ambiguous open state and is the primary way stale work reaches a
clean close.

### Close-Out

Close-Out fires on three triggers: explicit project completion, session-end
phrases ("wrap up", "done", "thanks"), and the session-start triage above. It
asks one default question — "Anything to note before I close this out?" — and on
a concrete note:

- records it via `add-feedback`;
- if the note names a repeatable creative rule, writes a structured
  `add-learning` (`candidate` -> `soft` -> `hard` via existing promotion fields);
- if the note names a *conductor* defect, writes an `add-learning` with
  `scope=conductor`, `learning-type=candidate`. This is a **staged conductor
  rule**, not a live edit (see "Promotion review surface").

All writes go through the CLI, append the required `events.jsonl` entry, and
scoped-sync. There is no new `learnings.md` and no new `MEMORY.md`; the
structured store is the memory equivalent.

### Conductor Rules: canonical block plus local sidecar

Conductor behavior corrections live at two tiers, mirroring how Agentic OS
separates shipped skill files from local findings so an OS upgrade never
overwrites them:

- **Canonical `## Rules`** in `skills/artist-os/SKILL.md`: dated one-line
  corrections that apply to every installation. Human-curated, edited only in
  deliberate batches, each batch followed by one re-bless. The conductor never
  appends to it live.
- **Local conductor rules** in `<workspace_library>/conductor-rules.md`: dated,
  append-only one-liners adopted from this installation's own findings. The
  conductor reads this file at session start, after the canonical Rules. It
  lives in the Workspace Library — the user-owned store that installs and
  upgrades never touch — so upgrading Artist OS can replace every skill file
  without losing local rules, and no host installer or updater needs to know
  the file exists. (A `SKILL.local.md` sibling inside the skill directory was
  considered and rejected: it would need per-host updater preservation logic,
  and plugin hosts restrict the skill directory per ADR 0008.) Like
  personal-library learnings, local rules are per Wondermint Root.

Local rules are additive: they may tighten behavior or record preferences, but
they must not disable canonical gates, approvals, or the never-auto-decide
class. On a direct conflict with the canonical file, the conductor surfaces the
conflict rather than silently choosing. Writes go through a minimal
`add-conductor-rule` verb (appends the dated line, marks the source candidate
applied, appends the event, scoped-syncs) so the "all writes through the CLI,
evented" invariant holds — no hand-edited workspace files.

This deliberately adopts only the minimal piece of the reference systems'
`SKILL.local.md` pattern — the upgrade-safe sidecar — and still rejects their
override load-order machinery and auto-commit hooks.

## Promotion review surface

A person unfamiliar with the system must be able to see what the loop has
learned and decide what to promote. The surface is two coordinated views over
the *existing* structured store — no new file type:

- **`review-learnings` (new read verb):** renders the pending queue in plain
  language, one item per block — what was observed (feedback text or learning
  rule text), which project it came from, its evidence, and a recommended action
  ("promote to a soft preference", "promote to a hard rule", "adopt as a local
  conductor rule", "nominate for the canonical Rules block", or "dismiss"). It
  applies nothing; it prints the exact command for each choice. This is the
  durable, discoverable place a maintainer can open at any time.
  Conductor-scoped candidates are rendered separately as "proposed changes to
  how the conductor works."
- **Conductor-presented review (primary for newcomers):** at session start or on
  request, the conductor walks the same queue conversationally in plain language
  and executes approved promotions via the CLI. The model is the friendly
  presenter; this is what makes the surface approachable without a dashboard.

**Three-tier conductor-rule promotion.** A staged conductor rule (a
`scope=conductor` candidate learning) never edits `SKILL.md` automatically.
Promotion climbs three tiers, each with a different stakes level and approver:

1. **Staged candidate** — captured automatically at Close-Out into the
   structured store. No behavior change yet.
2. **Local rule** — a reviewer (any user, including one unfamiliar with the
   internals) approves it via `review-learnings`, and `add-conductor-rule`
   appends it to `<workspace_library>/conductor-rules.md`. Low stakes:
   reversible, personal to this installation, no eval implications, survives
   upgrades.
3. **Canonical rule** — the repo maintainer batches proven local rules into
   `SKILL.md`'s `## Rules` block, marks the candidates applied, and re-blesses
   once. This is the only tier that changes shipped behavior or touches the
   hashed conductor file.

This satisfies human-in-the-loop promotion, gives newcomers a safe tier to act
on, keeps the eval lock stable during normal use, and keeps automation at
"some, not full-auto."

## What we deliberately do not adopt

Each rejected item names the reference system it comes from and why it is wrong
for Artist OS's lighter weight class.

| Rejected | From | Why not |
|---|---|---|
| pgvector / semantic recall, embeddings, per-turn Stop-hook capture | Agentic OS Command Centre | Redundant with a schema-backed store already queryable by structure; InfluencerOS deferred all of it. |
| SessionStart/Stop hooks and nightly/weekly cron | Agentic OS | Pure redundancy over the model-invoked skill layer; only automate *when* the loop runs. Layerable later without redesign. |
| Catalog-wide auto-editing of arbitrary skill files | Agentic OS | Artist OS has one conductor; scope any self-correction to its own Rules, human-gated. |
| Full `SKILL.local.md` override load-order + auto-commit hook | Agentic OS / InfluencerOS ADR 0014 | The override machinery and auto-commit hook stay out. The minimal piece — an upgrade-safe additive sidecar for local rules — **is** adopted (see "Conductor Rules"), because Artist OS is distributed (ADR 0008) and installed copies would otherwise lose local rules on every upgrade. |
| Byte-capped always-loaded `MEMORY.md` | Agentic OS / InfluencerOS | Nothing is force-loaded every session; the structured store is queried on demand, so no cap is needed. |
| Numeric performance-distillation engine (tension scoring, evidence-span floors, strength grading) | InfluencerOS `distill-creator-learning` | Existing `performance-signal` records at `equal_to_artist_feedback` weight suffice; do not block a light loop on Phase-2 work. |
| A dashboard / Command Centre over the loop | Agentic OS / InfluencerOS | `review-learnings`, `learnings-report`, and `status` stay CLI prints; the conductor is the human-facing surface. |
| `sync_meta` staleness table | (proposed then cut) | Read-path self-healing gives freshness without a second derived-state table that can itself desync (see below). |

## Database hardening

Learning writes ride on `sync`, so the loop is not finished until these land.
None of these touch `skills/artist-os/SKILL.md`, so none move the eval digest.
Where noted, the boundary is a direct port of InfluencerOS's proven code, not new
sync machinery.

### Event integrity and writer events

- **Per-manifest isolation.** Wrap each manifest's indexing in a `SAVEPOINT` with
  `try/except`; on failure roll back that project only, warn, and continue. Today
  the loop runs in one shared transaction with no per-project guard.
- **Parse-before-delete for events.** Read and parse all of `events.jsonl` into
  memory first (skip and warn on malformed lines), and only then delete and
  reinsert that project's event rows inside the savepoint. A missing *or*
  unreadable *or* mid-write events file must preserve the prior index. The
  current code deletes before it has a successful read, so a transient unreadable
  file zeroes indexed history.
- **Writers emit events.** `add-feedback`, `add-learning`, `add-performance-signal`,
  and `mark-learning-review-complete` must append the `events.jsonl` entry the
  storage contract already requires ("feedback received", "learning review
  marked", "performance signal imported"). Today they update files and the
  manifest but skip the event, which the event-indexing hardening alone would not
  fix.
- **`busy_timeout`.** Set `PRAGMA busy_timeout` in `connect()` so a concurrent
  reader or a second write does not fail with "database is locked" — the exact
  path that would otherwise leave files ahead of the index.

### Scoped sync

- **`sync --project <id>`** upserts one manifest (port InfluencerOS's per-scope
  `DELETE ... WHERE <scope> = ?` then reinsert boundary). Bare `sync` remains
  full-library — two spellings, not three.
- **Guard the missing-sweep to full sync only.** The sweep that marks every
  project not in the scanned set as `missing` must never run under
  `sync --project`; otherwise a single feedback write marks every other project
  missing. This is the most dangerous trap in the change and gets a dedicated
  test.
- **Switch the four writers to scoped sync.** This is the linchpin: a write
  reaches the index even when another project is corrupt, because it never scans
  that project.

### Read-path self-healing and rule-text surfacing

- **Self-heal before reading.** Learning-Review-at-Start scoped-syncs the
  projects it is about to surface immediately before reading them, so the index
  reflects the files it is trusting. This closes the read-trust gap, provides
  freshness (removing the need for `sync_meta`), and makes the loop degrade
  gracefully on a fresh clone where the DB does not exist yet.
- **Surface rule text.** `learnings-report` and `review-learnings` must emit the
  actual `learning_rule`, scope, and evidence by reading the referenced learning
  JSON, not just the ref IDs the `learning_refs` index stores. Without this the
  conductor gets IDs it cannot act on.

### Minimal status

- **`status [project_id]` (read-only, `mode=ro`).** With no argument: one row per
  project (id, stage, `learning_review_status`, pending count, staleness). This
  is what session-start triage enumerates open projects from, and the surface
  that proves the loop works end to end. The richer progress view
  (`resume_state`, blockers, `--json`) that `docs/progress.md` also lists as owed
  is **deferred** to separate work; it is not part of finalizing the loop.

## Eval-lock interaction

The conductor eval digest is a byte-hash of `skills/artist-os/SKILL.md` only.
Therefore:

- The database hardening and `review-learnings` / `status` verbs (all of the
  above) leave the digest untouched — no re-bless.
- Only wiring the loop into the conductor (Learning-Review-at-Start,
  session-start triage, Close-Out, the static `## Rules` block) changes
  `SKILL.md`, and that is done as one batched commit followed by exactly one
  re-bless. This also clears the pre-existing stale digest the audit already
  found on `main`.
- Staged conductor-rule candidates live in the structured store, and adopted
  local rules live in `<workspace_library>/conductor-rules.md` — both off
  `SKILL.md`, so neither ever churns the digest. Only tier-3 promotion (shipping
  a rule to everyone) touches the hashed file, and it re-blesses by design.
- The bless therefore guarantees the shipped baseline. Local rules are an
  explicitly unblessed overlay — the same standing as any user customization —
  bounded by the additive-only constraint above. The prose-integrity test pins
  that `SKILL.md` instructs the conductor to read the local rules file.

## Finish order and test plan

Each step ships with a verifiable success condition and tests added to
`tests/test_artist_os_db_storage.py`. Steps 1-3 do not touch `SKILL.md`.

**Step 1 — Event integrity and writer events.** Success: one corrupt manifest no
longer aborts sync; a missing, unreadable, or mid-write `events.jsonl` preserves
prior event rows; malformed event lines are skipped with a warning; the four
writers append their required events. Tests: corrupt-sibling isolation;
events-preserved-when-file-missing; events-preserved-when-file-unreadable;
malformed-line-late-in-file preserves prior rows; each writer emits its event.

**Step 2 — Scoped sync.** Success: writers scoped-sync; foreign rows survive; a
scoped sync does not mark foreign projects missing. Tests:
`scoped_sync_updates_only_target`; `scoped_sync_leaves_foreign_rows_intact`;
`scoped_sync_does_not_mark_foreign_projects_missing` (the trap guard);
`add_feedback_reaches_index_despite_corrupt_sibling` (load-bearing integration
proof).

**Step 3 — Read-path self-healing, rule text, minimal status, local rules
writer.** Success: `learnings-report` / `review-learnings` emit rule text,
scope, and evidence; a learning present in files but missing from the index is
still surfaced (self-heal proof); read verbs do not crash on a fresh clone with
no DB; `status` lists open projects with review state and staleness; the
connection is read-only; `add-conductor-rule` appends a dated line to
`<workspace_library>/conductor-rules.md`, marks the source candidate applied,
appends the event, and scoped-syncs. Tests: rule-text-surfaced;
learning-in-files-not-index-still-surfaced; fresh-clone-no-crash;
status-lists-open-projects; status-connection-is-read-only;
add-conductor-rule-appends-marks-and-events.

**Step 4 — Conductor wiring (`SKILL.md`, last).** Success: `SKILL.md` runs
Learning-Review-at-Start, session-start open-project triage, and Close-Out;
carries a static dated `## Rules` block; instructs the conductor to read
`<workspace_library>/conductor-rules.md` (additive, never gate-loosening) after
the canonical Rules; conductor-scoped Close-Out notes stage as candidates
rather than editing `SKILL.md`. Tests: a prose-integrity guard asserting the
sections exist and reference the learning verbs and the local rules read (a
near-zero-cost drift guard between full evals); the end-to-end round-trip
(`close_out -> event + scoped sync -> surfaced with rule text at next start ->
review complete -> status reflects`).

**Step 5 — One re-bless.** Required only because Step 4 changed `SKILL.md`. Run
`bin/artist-os-eval start`, execute a real conductor-behavior eval covering
Learning-Review-at-Start, triage, and Close-Out, then `bin/artist-os-eval bless`.
Batch all `SKILL.md` edits into Step 4's single commit; never re-bless for
wording-only churn.

## Consequences

- The self-improvement loop becomes functional and provable: a learning captured
  in one project is surfaced and applied at the start of a later one by the
  conductor itself, and a single command shows it captured, surfaced, synced, and
  reflected.
- Files-as-truth holds operationally, not just in principle: a corrupt sibling
  cannot block a write; a transient events file cannot zero history; a write that
  reaches JSON but not the index is healed at the next read rather than silently
  lost.
- The loop stays deliberately lighter than the reference systems — no hooks,
  cron, vector store, byte-capped memory, or distillation engine — while gaining
  the trigger and the human-gated, newcomer-facing promotion surface those
  systems have and Artist OS lacked.
- Promotion into the conductor is explicit and tiered: local adoption is safe,
  reversible, and requires no re-bless; shipping a rule to everyone is batched
  and re-blessed. The eval lock stays green during normal use and the blessed
  conductor never changes behind a bless.
- Upgrading Artist OS can replace every shipped skill file without losing an
  installation's adopted rules or learnings — local findings live in the
  Workspace Library, which upgrades never touch. Installed copies stay
  consistent with upstream while keeping their own corrections.
- The richer status/progress view remains owed follow-on work, tracked in
  `docs/progress.md`, and is intentionally out of scope here.
