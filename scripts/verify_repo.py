"""One-command repository verification.

Runs: required-file check, experiment-template check, package import,
ruff, pyright, and pytest. Exits non-zero on the first failing step.

Usage (from repository root):
    uv run python scripts/verify_repo.py
"""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "ROADMAP.md",
    "pyproject.toml",
    "uv.lock",
    ".python-version",
    "docs/STATUS.md",
    "docs/PROJECT.md",
    "docs/RESEARCH_METHOD.md",
    "docs/DATA_POLICY.md",
    "docs/GLOSSARY.md",
    "docs/QUESTION_ZERO.md",
    "docs/adr/README.md",
    "null_results/INDEX.md",
    "pearl_registry/INDEX.md",
    "literature/README.md",
    "literature/sources.yaml",
    "data/README.md",
    "notebooks/README.md",
    ".github/workflows/ci.yml",
)


def check_required_files() -> list[str]:
    return [f"missing required file: {p}" for p in REQUIRED_FILES if not (ROOT / p).is_file()]


def check_template() -> list[str]:
    from validate_experiment import REQUIRED_FILES as TEMPLATE_FILES  # noqa: PLC0415
    from validate_experiment import validate_experiment  # noqa: PLC0415

    template = ROOT / "experiments" / "_template"
    missing = [f"template missing: {n}" for n in TEMPLATE_FILES if not (template / n).is_file()]
    if missing:
        return missing
    # The template is intentionally unfilled (status PLANNED, placeholders), so only
    # the structural check on file presence and manifest shape is meaningful here.
    return [
        f"template structure: {p}"
        for p in validate_experiment(template)
        if not p.startswith("protocol.md lacks")
    ]


def check_import() -> list[str]:
    try:
        importlib.import_module("neural_echo")
    except ImportError as exc:
        return [f"cannot import neural_echo: {exc}"]
    return []


def run(step: str, cmd: list[str]) -> list[str]:
    print(f"== {step}: {' '.join(cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    return [] if result.returncode == 0 else [f"{step} failed (exit {result.returncode})"]


def main() -> int:
    sys.path.insert(0, str(ROOT / "scripts"))
    failures: list[str] = []

    print("== required files")
    failures += check_required_files()
    print("== experiment template")
    failures += check_template()
    print("== import")
    failures += check_import()

    failures += run("ruff", ["uv", "run", "ruff", "check", "."])
    failures += run("ruff format", ["uv", "run", "ruff", "format", "--check", "."])
    failures += run("pyright", ["uv", "run", "pyright"])
    failures += run("pytest", ["uv", "run", "pytest", "-q"])

    if failures:
        print("\nVERIFY FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nVERIFY OK: structure, template, import, ruff, pyright, pytest all passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
