"""Small JSON Schema validator for Artist OS records.

This intentionally implements the subset of JSON Schema used by this repo so
validation works without external dependencies. It is not a general-purpose
JSON Schema implementation.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent


@dataclass
class ValidationError(Exception):
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_schema(schema: dict[str, Any], root: dict[str, Any]) -> dict[str, Any]:
    ref = schema.get("$ref")
    if not ref:
        return schema
    if not ref.startswith("#/$defs/"):
        raise ValidationError("$ref", f"unsupported ref {ref!r}")
    key = ref.rsplit("/", 1)[1]
    try:
        return resolve_schema(root["$defs"][key], root)
    except KeyError as exc:
        raise ValidationError("$ref", f"missing ref {ref!r}") from exc


def type_matches(value: Any, expected: str | list[str]) -> bool:
    if isinstance(expected, list):
        return any(type_matches(value, item) for item in expected)
    checks = {
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, list),
        "string": lambda v: isinstance(v, str),
        "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "boolean": lambda v: isinstance(v, bool),
        "null": lambda v: v is None,
    }
    return checks[expected](value)


def validate(value: Any, schema: dict[str, Any], root: dict[str, Any], path: str = "$") -> None:
    schema = resolve_schema(schema, root)

    for subschema in schema.get("allOf", []):
        validate(value, subschema, root, path)

    if "if" in schema:
        try:
            validate(value, schema["if"], root, path)
        except ValidationError:
            pass
        else:
            if "then" in schema:
                validate(value, schema["then"], root, path)

    if "type" in schema and not type_matches(value, schema["type"]):
        raise ValidationError(path, f"expected {schema['type']}, got {type(value).__name__}")

    if "const" in schema and value != schema["const"]:
        raise ValidationError(path, f"expected const {schema['const']!r}")

    if "enum" in schema and value not in schema["enum"]:
        raise ValidationError(path, f"{value!r} is not one of {schema['enum']!r}")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            raise ValidationError(path, f"shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            raise ValidationError(path, f"longer than maxLength {schema['maxLength']}")
        if "pattern" in schema and not re.match(schema["pattern"], value):
            raise ValidationError(path, f"{value!r} does not match {schema['pattern']!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise ValidationError(path, f"{value!r} is below minimum {schema['minimum']!r}")
        if "maximum" in schema and value > schema["maximum"]:
            raise ValidationError(path, f"{value!r} is above maximum {schema['maximum']!r}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            raise ValidationError(path, f"has fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise ValidationError(path, f"has more than {schema['maxItems']} items")
        if "items" in schema:
            for index, item in enumerate(value):
                validate(item, schema["items"], root, f"{path}[{index}]")
        if "contains" in schema:
            match_count = 0
            for item in value:
                try:
                    validate(item, schema["contains"], root, path)
                except ValidationError:
                    continue
                match_count += 1
            min_contains = schema.get("minContains", 1)
            if match_count < min_contains:
                raise ValidationError(path, f"matches fewer than minContains {min_contains}")
            if "maxContains" in schema and match_count > schema["maxContains"]:
                raise ValidationError(path, f"matches more than maxContains {schema['maxContains']}")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                raise ValidationError(path, f"missing required field {key!r}")
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            if extras:
                raise ValidationError(path, f"unexpected fields {extras!r}")
        for key, item in value.items():
            if key in properties:
                validate(item, properties[key], root, f"{path}.{key}")

        if path == "$" and root.get("title") == "ReleasePackagePlan":
            validate_release_package_plan_contract(value)


def validate_release_package_plan_contract(record: dict[str, Any]) -> None:
    """Validate Album v1 cross-item invariants not expressible in our schema subset."""
    if record.get("package_subtype") != "album":
        return

    deliverables = record.get("deliverables", [])
    tracks = record.get("tracks", [])

    if record.get("album_cohesion_mode") == "arc_album":
        if not record.get("long_work_stewardship_record_ids", []):
            raise ValidationError(
                "$.long_work_stewardship_record_ids",
                "Album v1 arc_album requires at least one Long-Work Stewardship record id",
            )

        for track in tracks:
            track_id = track.get("track_id")
            album_beat_ref = track.get("album_beat_ref", {})
            if album_beat_ref.get("long_work_part_id") is None:
                raise ValidationError(
                    "$.tracks",
                    f"Album v1 arc_album track {track_id!r} requires a non-null long_work_part_id",
                )

    for deliverable_type in ["album_title", "album_description", "album_cover"]:
        matches = [
            deliverable for deliverable in deliverables
            if (
                deliverable.get("deliverable_type") == deliverable_type
                and deliverable.get("required") is True
                and deliverable.get("track_id") is None
            )
        ]
        if len(matches) != 1:
            raise ValidationError(
                "$.deliverables",
                f"Album v1 requires exactly one required package-level {deliverable_type} deliverable",
            )

    for track in tracks:
        track_id = track.get("track_id")
        sound_deliverables = [
            deliverable for deliverable in deliverables
            if (
                deliverable.get("deliverable_type") == "track_sound_prompt_plan"
                and deliverable.get("required") is True
                and deliverable.get("track_id") == track_id
            )
        ]
        if len(sound_deliverables) != 1:
            raise ValidationError(
                "$.deliverables",
                f"Album v1 track {track_id!r} requires exactly one required track_sound_prompt_plan deliverable",
            )

        cover_deliverables = [
            deliverable for deliverable in deliverables
            if (
                deliverable.get("deliverable_type") == "track_cover_image_prompt_plan"
                and deliverable.get("required") is True
                and deliverable.get("track_id") == track_id
            )
        ]
        if len(cover_deliverables) != 1:
            raise ValidationError(
                "$.deliverables",
                f"Album v1 track {track_id!r} requires exactly one required track_cover_image_prompt_plan deliverable",
            )

        cover_ids = {deliverable.get("deliverable_id") for deliverable in cover_deliverables}
        if track.get("track_cover_deliverable_id") not in cover_ids:
            raise ValidationError(
                "$.tracks",
                f"Album v1 track {track_id!r} track_cover_deliverable_id must reference its required Track Cover deliverable",
            )


def validate_file(schema_path: Path, data_path: Path) -> None:
    schema = load_json(schema_path)
    data = load_json(data_path)
    validate(data, schema, schema)


EXAMPLE_SCHEMA_MAP = {
    "asset-metadata.example.json": "asset-metadata.schema.json",
    "artist-meaning.example.json": "artist-meaning.schema.json",
    "beat-plan.example.json": "beat-plan.schema.json",
    "gate-decision.example.json": "gate-decision.schema.json",
    "image-medium-plan.example.json": "image-medium-plan.schema.json",
    "output-record.example.json": "output-record.schema.json",
    "prompt-branch-set.example.json": "prompt-branch-set.schema.json",
    "project-manifest.example.json": "project-manifest.schema.json",
    "project-feedback-log-entry.example.json": "project-feedback-log-entry.schema.json",
    "learning-record.example.json": "learning-record.schema.json",
    "performance-signal.example.json": "performance-signal.schema.json",
    "review-record.example.json": "review-record.schema.json",
    "sound-medium-plan.example.json": "sound-medium-plan.schema.json",
    "source-record.example.json": "source-record.schema.json",
    "creative-brief.example.json": "creative-brief.schema.json",
    "text-creative-brief.example.json": "text-creative-brief.schema.json",
    "text-prompt-plan.example.json": "prompt-plan.schema.json",
    "text-sound-creative-brief.example.json": "sound-creative-brief.schema.json",
    "text-sound-prompt-plan.example.json": "sound-prompt-plan.schema.json",
    "transformation-brief.example.json": "transformation-brief.schema.json",
}


FIXTURE_SCHEMA_MAP = {
    "source-record.json": "source-record.schema.json",
    "artist-meaning.json": "artist-meaning.schema.json",
    "output-acceptance-gate.json": "gate-decision.schema.json",
    "output-acceptance-waiver-gate.json": "gate-decision.schema.json",
    "image-style-gate.json": "gate-decision.schema.json",
    "image-detail-intensity-gate.json": "gate-decision.schema.json",
    "image-brief-approval-gate.json": "gate-decision.schema.json",
    "image-prompt-lock-gate.json": "gate-decision.schema.json",
    "suno-sound-work-type-gate.json": "gate-decision.schema.json",
    "suno-vocal-lyric-gate.json": "gate-decision.schema.json",
    "suno-brief-approval-gate.json": "gate-decision.schema.json",
    "suno-prompt-lock-gate.json": "gate-decision.schema.json",
    "text-writing-method-gate.json": "gate-decision.schema.json",
    "text-form-gate.json": "gate-decision.schema.json",
    "text-brief-approval-gate.json": "gate-decision.schema.json",
    "text-prompt-lock-gate.json": "gate-decision.schema.json",
    "text-draft-generation-approval-gate.json": "gate-decision.schema.json",
    "album-release-package-plan-approval-gate.json": "gate-decision.schema.json",
    "album-calibration-gate.json": "gate-decision.schema.json",
    "output-review-blocked-waived-record.json": "review-record.schema.json",
    "output-review-record.json": "review-record.schema.json",
    "fallback-review-record.json": "review-record.schema.json",
    "image-art-critic-review-record.json": "review-record.schema.json",
    "image-prompt-critic-review-record.json": "review-record.schema.json",
    "suno-sound-critic-review-record.json": "review-record.schema.json",
    "suno-prompt-critic-review-record.json": "review-record.schema.json",
    "text-writing-critic-review-record.json": "review-record.schema.json",
    "text-prompt-critic-review-record.json": "review-record.schema.json",
    "album-pre-calibration-mixed-media-critic-review-record.json": "review-record.schema.json",
    "symbology-gate.json": "gate-decision.schema.json",
    "transformation-brief.json": "transformation-brief.schema.json",
    "beat-plan.json": "beat-plan.schema.json",
    "image-medium-plan.json": "image-medium-plan.schema.json",
    "output-record.json": "output-record.schema.json",
    "output-record-draft.json": "output-record.schema.json",
    "output-record-clear-writing.json": "output-record.schema.json",
    "output-record-human-voice.json": "output-record.schema.json",
    "creative-brief.json": "creative-brief.schema.json",
    "text-creative-brief.json": "text-creative-brief.schema.json",
    "sound-medium-plan.json": "sound-medium-plan.schema.json",
    "sound-creative-brief.json": "sound-creative-brief.schema.json",
    "prompt-plan.json": "prompt-plan.schema.json",
    "prompt-branch-set.json": "prompt-branch-set.schema.json",
    "sound-prompt-plan.json": "sound-prompt-plan.schema.json",
    "sound-prompt-plan-phonetic-vocals.json": "sound-prompt-plan.schema.json",
    "text-generation-plan.json": "text-generation-plan.schema.json",
    "text-medium-plan.json": "text-medium-plan.schema.json",
    "video-medium-plan.json": "video-medium-plan.schema.json",
    "review-record.json": "review-record.schema.json",
    "album-release-package-plan.json": "release-package-plan.schema.json",
    "asset-metadata.json": "asset-metadata.schema.json",
    "project-manifest.json": "project-manifest.schema.json",
    "project-feedback-log-entry.json": "project-feedback-log-entry.schema.json",
    "learning-record.json": "learning-record.schema.json",
    "performance-signal.json": "performance-signal.schema.json",
    "foundation-stewardship-record.json": "long-work-stewardship-record.schema.json",
    "album-stewardship-record.json": "long-work-stewardship-record.schema.json",
    "image-series-stewardship-record.json": "long-work-stewardship-record.schema.json",
    "text-stewardship-record.json": "long-work-stewardship-record.schema.json",
}


def iter_validation_targets(include_fixtures: bool = True) -> list[tuple[Path, Path]]:
    targets: list[tuple[Path, Path]] = []
    for filename, schema_name in EXAMPLE_SCHEMA_MAP.items():
        data_path = REPO_ROOT / "examples" / filename
        if data_path.exists():
            targets.append((REPO_ROOT / "schemas" / schema_name, data_path))
    if include_fixtures:
        fixtures_root = REPO_ROOT / "tests" / "fixtures"
        for data_path in sorted(fixtures_root.rglob("*.json")):
            schema_name = FIXTURE_SCHEMA_MAP.get(data_path.name)
            if schema_name:
                targets.append((REPO_ROOT / "schemas" / schema_name, data_path))
    return targets
