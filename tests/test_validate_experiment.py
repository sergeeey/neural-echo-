import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate_experiment import main, validate_experiment  # noqa: E402

TEMPLATE = ROOT / "experiments" / "_template"


def _copy(tmp_path: Path) -> Path:
    dest = tmp_path / "exp"
    shutil.copytree(TEMPLATE, dest)
    return dest


def _set_status(folder: Path, status: str) -> None:
    manifest = folder / "manifest.yaml"
    text = manifest.read_text(encoding="utf-8")
    new = text.replace("status: PLANNED", f"status: {status}")
    # WHY: fail loudly if the substitution did not apply, so the test cannot
    # silently run with the original status.
    assert new != text, "status line not found in manifest template"
    manifest.write_text(new, encoding="utf-8")


def _remove_manifest_key(folder: Path, key: str) -> None:
    # WHY: drop the top-level key together with its indented children, otherwise
    # the remaining children make the YAML invalid and the test checks the wrong thing.
    manifest = folder / "manifest.yaml"
    kept: list[str] = []
    skipping = False
    found = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        is_top_level = bool(line) and not line[0].isspace()
        if is_top_level:
            skipping = line.startswith(f"{key}:")
            found += skipping
        if not skipping:
            kept.append(line)
    assert found == 1, f"top-level key {key!r} not found exactly once"
    manifest.write_text("\n".join(kept) + "\n", encoding="utf-8")


def test_template_is_valid_when_planned(tmp_path: Path) -> None:
    assert validate_experiment(_copy(tmp_path)) == []


def test_missing_file_is_reported(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    (folder / "controls.md").unlink()
    assert "missing file: controls.md" in validate_experiment(folder)


def test_invalid_status_is_reported(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    _set_status(folder, "SUCCESS")
    assert any("invalid status" in p for p in validate_experiment(folder))


def test_unhashable_status_is_a_finding_not_a_crash(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    manifest = folder / "manifest.yaml"
    text = manifest.read_text(encoding="utf-8")
    manifest.write_text(text.replace("status: PLANNED", "status: [FROZEN]"), encoding="utf-8")
    problems = validate_experiment(folder)
    assert any(p.startswith("invalid status") for p in problems)


@pytest.mark.parametrize(
    "status", ["FROZEN", "RUNNING", "SUPPORTED", "NOT_SUPPORTED", "INVALIDATED"]
)
def test_frozen_or_later_status_requires_heading_marker(tmp_path: Path, status: str) -> None:
    folder = _copy(tmp_path)
    (folder / "protocol.md").write_text("no marker here\n", encoding="utf-8")
    _set_status(folder, status)
    assert any("FROZEN PROTOCOL" in p for p in validate_experiment(folder))


def test_marker_in_prose_does_not_count(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    (folder / "protocol.md").write_text(
        "We mention FROZEN PROTOCOL in prose only.\n", encoding="utf-8"
    )
    _set_status(folder, "FROZEN")
    assert any("FROZEN PROTOCOL" in p for p in validate_experiment(folder))


def test_frozen_status_passes_with_heading_marker(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    (folder / "protocol.md").write_text("## FROZEN PROTOCOL\n\nfixed.\n", encoding="utf-8")
    _set_status(folder, "FROZEN")
    assert validate_experiment(folder) == []


def test_missing_manifest_field_is_reported(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    _remove_manifest_key(folder, "dataset")
    assert "manifest missing field: dataset" in validate_experiment(folder)


def test_non_mapping_manifest_is_reported(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    (folder / "manifest.yaml").write_text("- just\n- a list\n", encoding="utf-8")
    assert validate_experiment(folder) == ["manifest.yaml must be a mapping"]


def test_non_utf8_protocol_is_reported_not_raised(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    (folder / "protocol.md").write_bytes(b"\xff\xfe bad bytes")
    _set_status(folder, "FROZEN")
    assert any("not UTF-8" in p for p in validate_experiment(folder))


def test_main_exit_codes(tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    assert main(["validate_experiment.py", str(folder)]) == 0
    _set_status(folder, "SUCCESS")
    assert main(["validate_experiment.py", str(folder)]) == 1
    assert main(["validate_experiment.py"]) == 2
