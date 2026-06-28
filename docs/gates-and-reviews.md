# Gates And Reviews

This is the canonical Artist OS contract for gates, critic roles, reviewer roles, and review execution.

Use this file before adding or changing a journey. Medium-specific docs can add local gates, but shared gate order and review rules live here. The detailed per-gate and per-role definitions live in per-topic files under `docs/gates/`; this file holds the shared order, the cross-cutting rules, and the pointers to those files.

## Shared Gate Order

The default cross-medium journey uses this gate order:

```text
Routing Gate
  -> Meaning Confirmation Gate
  -> Research Grounding Gate, when timely or public-facing work may need current evidence
  -> Interpretation Gate
  -> Story Gate
  -> Story Critic Review
  -> Story Approval Gate
  -> Long-Work Readiness / Checkpoints, when the work is cumulative
  -> Medium Gates
  -> Format Length Gate, when the artist overrides the default length standard
  -> Medium Critic Review
  -> Brief Approval Gate
  -> Prompt Critic Review
  -> Prompt Branch Gate, when curator batches are requested
  -> Prompt Lock Gate
  -> Review Presentation Gate, for written Output Artifacts
  -> Generation Approval Gate, or Draft Generation Approval Gate for text drafting
  -> Output Critic Review
  -> Output Acceptance Gate
```

Provider-backed generation always requires explicit approval. Drafting briefs, boards, prompt plans, lyrics, scripts, shot lists, comparison boards, or other dry-run artifacts is allowed.

## Standing Sub-Agent Authorization

Artist OS has standing user authorization to spawn bounded internal sub-agents automatically for mandatory reviews, validation, drafting passes, audits, and approved orchestration patterns. The conductor must not ask for separate approval before each sub-agent.

This authorization does not apply to provider-backed generation, paid actions, uploads, destructive actions, artist-facing gate approvals, waivers, or output acceptance. Those actions still require their own explicit artist decisions.

If the host cannot spawn a sub-agent or the active tool policy blocks spawning despite this standing authorization, the conductor may use the documented fallback separated review pass and must record degraded execution.

## Gate Completion Rule

A gate is complete, an approval given, a waiver granted, or an option selected only when it comes from an explicit artist turn: an actual artist response in the conversation. The agent must not infer approval from silence, treat its own recommendation as the artist's answer, self-approve, or assume the artist would obviously want a choice. "Obvious," "low-risk," "trivial," or "an obvious fix" does not waive this requirement. An obvious choice is still the artist's choice.

Recording a Gate Decision, approval, selection, or waiver the artist did not actually make is forbidden. It fabricates provenance and breaks the audit trail that every downstream record inherits.

This rule applies to every gate in this document, including Brief Approval, Series/Sequence approval, Generation Approval, Draft Generation Approval, and blocking-finding waivers.

## Continuation Rule

After an explicit artist turn completes a gate, answers a Decision Interview question, or corrects a project detail, the agent must not stop with only acknowledgement or persistence status. It must either:

- continue immediately into the next unlocked pipeline step, or
- ask the next concrete required gate or Decision Interview question when artist input is still the blocker.

This is especially important for small confirmations and corrections such as spelling, terminology, rights policy, genre, vocal mode, calibration details, or approval of a recommended answer. Recording the answer is required, but recording alone is not a complete artist-facing turn. The artist should never have to ask "what is next?" to recover the workflow.

## Video Format Gate

The Video Format Gate is one of the Medium Gates; its full definition lives in `docs/gates/canonical-gates.md` → "Medium Gate". The story-shape requirement is load-bearing and stays here:

For the Video Format Gate, the recommendation must include the story type and Beat Plan shape before the artist is asked to choose. State what the story is, how many smallest Story Beats or Story Movements it appears to need, the recommended video format, and why that format fits better than nearby alternatives. Do not start with a broad video format menu when the Reference or Beat Plan gives enough material to recommend.

## Topic Files

The detailed definitions moved to per-topic files. Load only the one the current step needs:

- Canonical Gates — every gate definition and its completion rule, from the Routing Gate through the Output Acceptance Gate (including the Medium Gate and its Video Format Gate detail) — `docs/gates/canonical-gates.md`
- Critic Roles And Writing Method Reviewers — Meaning Reviewer, Story Critic, Art Critic, Video Critic, Sound Critic, Writing Critic, Mixed-Media Critic, Long-Work Reviewer, Prompt Critic, Output Critic, and the Fragment / Beat / Shape writing-method reviewers — `docs/gates/critic-roles.md`
- Review Execution And Blocking Findings — the mandatory bounded sub-agent review rule, the Review Record contract, the fallback separated pass, and the blocking-finding waiver rule — `docs/gates/review-execution.md`
