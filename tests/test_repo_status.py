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


def test_missing_status_is_reported_not_raised(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(verify_repo, "ROOT", tmp_path)
    assert verify_repo.check_status() == ["docs/STATUS.md missing"]
