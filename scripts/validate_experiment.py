"""Structural validator for experiment folders.

Checks structure only: required files exist, manifest has required fields,
status is in the allowed vocabulary, and the FROZEN PROTOCOL marker exists
when the status requires it. It does NOT verify scientific integrity,
checksums, or provenance; those checks are not implemented yet
(see data/README.md).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_FILES = (
    "question.md",
    "estimand.md",
    "claim.md",
    "alternative_hypotheses.md",
    "protocol.md",
    "controls.md",
    "manifest.yaml",
    "decision.md",
)

REQUIRED_MANIFEST_FIELDS = (
    "experiment_id",
    "creation_date",
    "git_commit",
    "dataset",
    "code_provenance",
    "random_seeds",
    "environment",
    "outputs",
    "status",
)

VALID_STATUSES = frozenset(
    {
        "PLANNED",
        "FROZEN",
        "RUNNING",
        "SUPPORTED",
        "NOT_SUPPORTED",
        "INCONCLUSIVE",
        "INVALIDATED",
    }
)

# Statuses at or after which the protocol must already be frozen.
FROZEN_REQUIRED_STATUSES = VALID_STATUSES - {"PLANNED"}

FROZEN_MARKER = "FROZEN PROTOCOL"


def _marker_present(protocol_text: str) -> bool:
    # WHY: match the marker as a heading line, not a substring, so that prose
    # mentioning the phrase cannot satisfy the freeze requirement.
    return any(
        line.strip().startswith("## " + FROZEN_MARKER) for line in protocol_text.splitlines()
    )


def validate_experiment(folder: Path) -> list[str]:
    """Return a list of structural problems; an empty list means the structure is valid."""
    problems: list[str] = []
    if not folder.is_dir():
        return [f"not a directory: {folder}"]

    for name in REQUIRED_FILES:
        if not (folder / name).is_file():
            problems.append(f"missing file: {name}")

    manifest_path = folder / "manifest.yaml"
    if manifest_path.is_file():
        try:
            manifest: Any = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        except (yaml.YAMLError, UnicodeDecodeError) as exc:
            return problems + [f"manifest.yaml is not readable YAML: {exc}"]
        if not isinstance(manifest, dict):
            return problems + ["manifest.yaml must be a mapping"]

        for field in REQUIRED_MANIFEST_FIELDS:
            if field not in manifest:
                problems.append(f"manifest missing field: {field}")

        status = manifest.get("status")
        # WHY: check the type before set membership; an unhashable value such as a
        # list would otherwise raise TypeError instead of producing a finding.
        if not isinstance(status, str) or status not in VALID_STATUSES:
            problems.append(f"invalid status: {status!r}")
        elif status in FROZEN_REQUIRED_STATUSES:
            protocol = folder / "protocol.md"
            if protocol.is_file():
                try:
                    text = protocol.read_text(encoding="utf-8")
                except UnicodeDecodeError as exc:
                    problems.append(f"protocol.md is not UTF-8: {exc}")
                else:
                    if not _marker_present(text):
                        problems.append(
                            f"protocol.md lacks '## {FROZEN_MARKER}' heading but status is {status}"
                        )

    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_experiment.py <experiment-folder>", file=sys.stderr)
        return 2
    problems = validate_experiment(Path(argv[1]))
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1
    print("OK: structure valid (structural check only; no integrity verification)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
