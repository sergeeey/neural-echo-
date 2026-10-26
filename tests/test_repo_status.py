import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
# WHY: scripts/ is not a package; add it to sys.path so the validator module can be imported.
sys.path.insert(0, str(ROOT / "scripts"))

import verify_repo  # noqa: E402  (import must follow the sys.path insert above)


def test_status_document_has_required_sections() -> None:
    assert verify_repo.check_status() == []


def test_truncated_status_is_reported(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # WHY: prove the check can fail, not only that it passes on the real file.
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "STATUS.md").write_text("# STATUS\n\n## Current phase\n", encoding="utf-8")
    monkeypatch.setattr(verify_repo, "ROOT", tmp_path)
    problems = verify_repo.check_status()
    assert "docs/STATUS.md missing section: ## Blockers" in problems
    assert "docs/STATUS.md missing section: ## Next 3 actions" in problems


def test_broken_experiment_folder_fails_the_repo_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # WHY: a real experiment folder that is malformed must surface as a named finding.
    exp = tmp_path / "experiments" / "20991231-broken"
    exp.mkdir(parents=True)
    monkeypatch.setattr(verify_repo, "ROOT", tmp_path)
    findings = verify_repo.check_experiments()
    assert any(f.startswith("20991231-broken: missing file:") for f in findings)


def test_experiment_id_must_match_folder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    template = ROOT / "experiments" / "_template"
    exp = tmp_path / "experiments" / "20991231-right-name"
    shutil.copytree(template, exp)
    manifest = exp / "manifest.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "experiment_id: null", "experiment_id: 20991231-other-name"
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(verify_repo, "ROOT", tmp_path)
    assert any("does not match folder name" in f for f in verify_repo.check_experiments())


def test_missing_experiments_dir_is_a_finding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(verify_repo, "ROOT", tmp_path)
    assert verify_repo.check_experiments() == ["experiments/ directory missing"]


def test_missing_status_is_reported_not_raised(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(verify_repo, "ROOT", tmp_path)
    assert verify_repo.check_status() == ["docs/STATUS.md missing"]
