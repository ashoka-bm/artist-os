# Draft Journey: UGC Campaign Content Factory

Status: research draft.

## End Product

A batch of short UGC or ad videos, plus optional image assets, organized as a campaign plan.

## Likely Inputs

- Product image or URL.
- Brand or product description.
- Campaign size.
- Campaign dates.
- Target platform or ad use.
- Avatar strategy.
- Optional brand kit, ad reference, hooks, settings, or product variants.

## Prompt Needs

- Classify the product category.
- Pick relevant preset families.
- Build a campaign plan before generation.
- Keep each clip inside provider duration limits.
- Group videos by format bucket.
- Ask permission before each paid generation batch.
- Track failed rows for retry.
- Optionally analyze finished clips for hook and retention.

## Draft Format Buckets

- UGC entertainment.
- Street interview.
- Unboxing.
- Product review.
- ASMR or sound-led product handling.
- TV spot, hyper-motion, virtual try-on, and wild-card concepts when the product supports them.

## Known Risks

- The plan proposes clips longer than the provider allows.
- Unsupported hooks or settings are invented instead of selected from provider lists.
- Product visibility is weak.
- Avatar strategy is missing and each clip casts a new presenter.
- Batch generation runs without explicit approval.
- Campaign metrics and generated assets are not tied back to records.

## Artist OS Mapping

This journey likely belongs outside the core Video Journey. It may map to a future campaign package plan, provider adapter, Output Records, Performance Signals, and approval gates.
