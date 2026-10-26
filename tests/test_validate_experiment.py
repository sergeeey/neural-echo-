import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate_experiment import validate_experiment  # noqa: E402

TEMPLATE = ROOT / "experiments" / "_template"


def _copy(tmp_path: Path) -> Path:
    dest = tmp_path / "exp"
    shutil.copytree(TEMPLATE, dest)
    return dest


def _set_status(folder: Path, status: str) -> None:
    manifest = folder / "manifest.yaml"
    text = manifest.read_text(encoding="utf-8")
    manifest.write_text(text.replace("status: PLANNED", f"status: {status}"), encoding="utf-8")


def test_template_has_no_structural_problems_when_planned(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    assert validate_experiment(folder) == []


def test_missing_file_is_reported(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    (folder / "controls.md").unlink()
    assert "missing file: controls.md" in validate_experiment(folder)


def test_invalid_status_is_reported(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    _set_status(folder, "SUCCESS")
    assert any("invalid status" in p for p in validate_experiment(folder))


@pytest.mark.parametrize("status", ["FROZEN", "SUPPORTED", "NOT_SUPPORTED"])
def test_frozen_status_requires_marker(tmp_path: Path, status: str) -> None:
    folder = _copy(tmp_path)
    (folder / "protocol.md").write_text("no marker here\n", encoding="utf-8")
    _set_status(folder, status)
    assert any("FROZEN PROTOCOL" in p for p in validate_experiment(folder))


def test_frozen_status_passes_with_marker(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    _set_status(folder, "FROZEN")
    assert validate_experiment(folder) == []


def test_missing_manifest_field_is_reported(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    manifest = folder / "manifest.yaml"
    lines = [
        ln
        for ln in manifest.read_text(encoding="utf-8").splitlines()
        if not ln.startswith("checksum")
    ]
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # 'dataset' is a mapping; removing it entirely must be reported.
    manifest.write_text(
        "\n".join(
            ln
            for ln in manifest.read_text(encoding="utf-8").splitlines()
            if not ln.startswith(("dataset:", "  name:", "  version:", "  checksum_sha256:"))
        )
        + "\n",
        encoding="utf-8",
    )
    assert "manifest missing field: dataset" in validate_experiment(folder)
