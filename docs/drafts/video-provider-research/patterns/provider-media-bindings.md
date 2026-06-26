# Draft Pattern: Provider Media Bindings

Status: research draft.

Provider adapters need a layer that maps Artist OS records and assets to provider-specific media roles. The AI Influencer repository shows several such roles: image, start image, end image, audio, product, avatar, hook, setting, and video-analysis input.

## Draft Principle

Core Artist OS records should describe what an asset means. Provider bindings should describe how that asset is passed to a provider.

## Binding Examples

- Identity image -> provider `image` or start frame.
- Reference image -> provider `image`, with scope as subject, style, object, or scene.
- Approved storyboard still -> provider `start_image`.
- Ending keyframe -> provider `end_image`.
- Voice recording -> provider `audio`.
- Product image -> Marketing Studio product media or product id.
- Presenter identity -> avatar or Soul reference.
- Finished clip -> Virality Predictor video input.

## What The Binding Should Store

- Provider target.
- Source asset or Output Record id.
- Provider role.
- Provider upload id or job id, when generated.
- Scope note: identity, wardrobe, product, start frame, audio, analysis input.
- Approval or gate reference for paid generation.

## Risks

- Core schema gets polluted with one provider's role names.
- Uploaded media ids are lost and the same media gets re-uploaded unnecessarily.
- A provider role is wrong for the selected model.
- Audio references are confused with provider-generated audio flags.
