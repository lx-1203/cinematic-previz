"""Validate generation-segment durations without rewriting the production plan.

Expected input:
{
  "generation_segments": [
    {"segment_id": "...", "logical_shot_id": "...", "duration_seconds": 6}
  ]
}

Optional plan constraints use:
{
  "duration_constraints": {"min_seconds": 4, "max_seconds": 8}
}

CLI --min/--max override plan constraints. The default is 4-8 seconds.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def validate(data: dict, min_seconds: float, max_seconds: float) -> dict:
    errors = []
    segments = data.get("generation_segments")
    if not isinstance(segments, list) or not segments:
        errors.append(
            {
                "code": "SCHEMA",
                "path": "generation_segments",
                "message": "Expected a nonempty array",
            }
        )
        segments = []
    identifiers = set()
    durations = []
    for index, item in enumerate(segments):
        path = f"generation_segments.{index}"
        if not isinstance(item, dict):
            errors.append(
                {"code": "SCHEMA", "path": path, "message": "Expected an object"}
            )
            continue
        identifier = item.get("segment_id")
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append(
                {
                    "code": "SCHEMA",
                    "path": path + ".segment_id",
                    "message": "Expected a nonempty string",
                }
            )
        elif identifier in identifiers:
            errors.append(
                {
                    "code": "DUPLICATE_ID",
                    "path": path + ".segment_id",
                    "message": identifier,
                }
            )
        else:
            identifiers.add(identifier)
        duration = item.get("duration_seconds")
        if isinstance(duration, bool) or not isinstance(duration, (int, float)):
            errors.append(
                {
                    "code": "SCHEMA",
                    "path": path + ".duration_seconds",
                    "message": "Expected a number",
                }
            )
            continue
        durations.append(duration)
        if duration < min_seconds or duration > max_seconds:
            errors.append(
                {
                    "code": "DURATION_OUT_OF_RANGE",
                    "path": path + ".duration_seconds",
                    "message": (
                        f"{identifier or index}: {duration:g}s is outside "
                        f"{min_seconds:g}-{max_seconds:g}s"
                    ),
                }
            )
    return {
        "status": "failed" if errors else "passed",
        "constraints": {
            "min_seconds": min_seconds,
            "max_seconds": max_seconds,
            "applies_to": "each generation segment",
        },
        "segment_count": len(segments),
        "duration_min": min(durations) if durations else None,
        "duration_max": max(durations) if durations else None,
        "errors": errors,
        "note": "Passing timing validation does not prove visual or audio quality.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--min", dest="min_seconds", type=float)
    parser.add_argument("--max", dest="max_seconds", type=float)
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        data = json.loads(args.plan.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as error:
        print(
            json.dumps(
                {
                    "status": "invalid_input",
                    "errors": [
                        {"code": "INPUT", "path": str(args.plan), "message": str(error)}
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2
    configured = data.get("duration_constraints", {})
    min_seconds = (
        args.min_seconds
        if args.min_seconds is not None
        else configured.get("min_seconds", 4)
    )
    max_seconds = (
        args.max_seconds
        if args.max_seconds is not None
        else configured.get("max_seconds", 8)
    )
    if (
        not isinstance(min_seconds, (int, float))
        or isinstance(min_seconds, bool)
        or not isinstance(max_seconds, (int, float))
        or isinstance(max_seconds, bool)
        or min_seconds < 0
        or max_seconds < min_seconds
    ):
        print(
            json.dumps(
                {
                    "status": "invalid_input",
                    "errors": [
                        {
                            "code": "CONSTRAINT",
                            "path": "duration_constraints",
                            "message": "Require 0 <= min <= max",
                        }
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2
    report = validate(data, float(min_seconds), float(max_seconds))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
