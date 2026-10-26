"""One-command repository verification.

Runs every check and reports all failures at the end, so one run shows the full
picture. Checks: required files, experiment-template structure, package import,
ruff lint, ruff format, pyright, pytest.

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
    # The template is unfilled and status PLANNED, so the full structural check applies as-is.
    return [f"template structure: {p}" for p in validate_experiment(template)]


def check_import() -> list[str]:
    try:
        importlib.import_module("neural_echo")
    except ImportError as exc:
        return [f"cannot import neural_echo: {exc}"]
    return []


def run(step: str, cmd: list[str]) -> list[str]:
    print(f"== {step}: {' '.join(cmd)}", flush=True)
    try:
        result = subprocess.run(cmd, cwd=ROOT, check=False)
    except FileNotFoundError:
        return [f"{step}: command not found ({cmd[0]}); install uv first"]
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
