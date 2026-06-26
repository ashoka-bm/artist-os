# Higgsfield Draft Notes

Status: research draft.

Higgsfield appears in the current references as the user-facing tool or workflow environment for creating image-conditioned and audio-conditioned short videos. The references often pair Higgsfield with Seedance 2.0 prompt behavior, so this file should separate Higgsfield-specific UI requirements from Seedance-specific prompt behavior as more material arrives.

## Known From Current References

- The workflow expects uploaded image and audio references.
- Prompts may use provider tags such as image and audio handles.
- Creator-clone use cases depend on identity reference, exact transcript, and lip-sync audio.
- The examples focus on short clips, usually 5 to 15 seconds.
- Higgsfield Supercomputer may support higher-level prompt requests that ask for complete scene sequences or motion-graphics packages.
- The AI Influencer repository uses Higgsfield as both a generation provider and a workflow surface for images, video, Marketing Studio ads, avatars, products, hooks, settings, and video analysis.
- Provider media roles differ by model; the adapter layer must bind Artist OS assets to the selected model's accepted roles.
- Marketing Studio campaign work is preset-driven and should not be treated as free-form Seedance prompting.

## Unknown

- Which prompt rules belong to Higgsfield itself.
- Which rules belong to the underlying model.
- How Higgsfield names or stores uploaded references.
- What output settings, duration limits, aspect ratios, seeds, or cost controls matter.
- Whether Higgsfield Supercomputer reliably renders exact text for motion-graphics cards.
- Whether scene sequences should be prompted as one request or separate provider generations.
- Which Marketing Studio capabilities and preset lists are available in the user's account at generation time.
- Whether AI influencer identity should use Higgsfield Soul, GPT Image 2, or another model as the canonical first step.

## Draft Role

Higgsfield should be treated as a future provider target or host context after storyboard approval. It should not redefine the neutral Video Journey.

For campaign and influencer workflows, Higgsfield may also become a separate commercial-content adapter that consumes identity kits, product records, and package plans.
