# Higgsfield / Seedance Prompt Pack Analysis

## Reference

- Reference id: `ref_higgsfield_seedance_prompt_pack_001`
- Title: `Dan Kieft's Create Insane AI Videos of Yourself Using Seedance 2.0 Prompt Pack`
- Source path: `/Users/ashokaji/.codex/attachments/39e4be8a-f5ab-4bb4-832d-2031457f937d/pasted-text.txt`
- Date analyzed: 2026-06-24
- Provider or platform: Higgsfield workflow targeting Seedance 2.0-style video generation
- Reference type: prompt pack and examples
- Reuse policy: use for analysis and example coverage; do not copy examples into production docs

## What It Is

This reference is a set of example prompts for creator-clone videos. It is less authoritative than the master guide because it contains older prompt habits that the later guide appears to refine. Its value is coverage: it shows concrete content types that the future draft grid should support.

## Video Types

- Airport side-profile walk-through with suitcase.
- Handheld outdoor vlog one-take.
- Walk-and-set-down vlog for voice consistency.
- Studio talking head for voice consistency.
- Hotel-room handheld tour driven by avatar reference and audio.

## Assumed Inputs

- Avatar or identity reference image.
- Optional prop image, such as luggage.
- Audio file for lip-sync.
- Transcript for spoken content.
- Short target duration, often 5 to 15 seconds.
- A provider UI that accepts image and audio tags.

## Prompt Structure

The examples use the same broad prompt sections as the master guide: format, subject, wardrobe, environment, style anchor, delivery, logic rule, negative prompt, and action. They show short-form creator-content prompts rather than general film storyboards.

The examples help identify expected user requests. A user may ask for a scene by giving a provider, reference image, audio tag, setting, duration, one-take requirement, and transcript. The prompt builder must translate that into shot family, reference scope, action density, camera behavior, and delivery rules.

## Reusable Patterns

- Start with a concrete video type and duration.
- Use the identity image as the visual authority for the subject.
- Include exact wardrobe and prop details only when they matter.
- Keep one-take scenes in prose flow rather than time-sliced mini-scenes.
- For creator-clone tests, choose medium close-up or close framing when face fidelity matters.
- For tour videos, map the transcript to physical reveals without overloading the duration.

## Failure Modes

The prompt pack itself does not analyze failures deeply, but it exposes likely risks:

- Audio may become muffled if delivery describes microphone tone too strongly.
- Duplicate camera or phone artifacts may appear in set-down vlogs.
- "Casey Neistat-style" may carry visible-camera baggage.
- Full-body airport shots may reduce face fidelity.
- Alternative surfaces such as "sidewalk, park bench, or low ledge" leave the provider too much choice.
- Typos and loose phrasing may weaken prompt control.

## Conflicts

The prompt pack includes patterns the master guide later discourages. Treat the master guide as the current source for provider-specific corrections. This prompt pack should supply sample categories and regression cases, not final wording.

## Mapping To Artist OS

- Each example maps to a compact `Video Medium Plan` with one scene and one or more storyboard shots.
- The hotel-room example maps well to a future `handheld-vlog-tour` journey.
- Voice-consistency examples map to dialogue-led audio posture and exact transcript preservation.
- Airport and b-roll examples map to static observational or single-shot b-roll journeys.

## Draft Fields To Consider

- `sample_type`
- `transcript_exact_text`
- `tour_reveal_order`
- `identity_reference_required`
- `prop_reference_required`
- `face_fidelity_priority`
- `camera_placement_risk`

## Open Questions

- Does Higgsfield itself add conventions beyond Seedance prompt syntax?
- Which sample types should become first-class draft journeys?
- How should the system decide when a transcript is too dense for the requested duration?
- Should voice-consistency tests be a journey type, a QA mode, or a provider export option?
