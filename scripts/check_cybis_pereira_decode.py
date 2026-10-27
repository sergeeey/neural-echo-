"""Recompute r² of the authors' speed decoders from their published test outputs (read-only).

Data: Cybis Pereira et al., Zenodo 15476373 (CC BY 4.0), derivatives `decode-speed` and
`interanimal-decode-speed`, fetched into git-ignored `data/raw/cybis_pereira_2026/`.

What this checks: whether r² computed from the authors' own `predicted` / `actual` test
columns reproduces the maxima quoted in their preprint text (intra-animal up to 0.6;
inter-animal up to 0.36). It does NOT refit the decoder from raw fUS data.

Negative control: circular time-shifts of `predicted` within each test file (seed fixed,
shifts >= SHIFT_MIN frames). Reported as the null mean and sd, z, and p. A shift null is
a check on temporal alignment only; it is not a leakage test.

Regressor vs dummy: paired per animal and test length n, with a circular-block bootstrap
(block = SHIFT_MIN frames) of the r² difference.

Duplicates: an inter-animal dummy row whose (animal, n, r²) equals an intra-animal dummy
row is flagged and excluded from the aggregates. Byte-different files with identical
r² and n are not treated as independent evidence; the cause is UNKNOWN.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data" / "raw" / "cybis_pereira_2026"
SEED = 20261027
N_SHIFT = 1000
N_BOOT = 1000
SHIFT_MIN = 200  # frames; excludes near-zero circular shifts from the null
PAPER_MAX_INTRA = 0.6
PAPER_MAX_INTER = 0.36


def read_pred_actual(path: Path) -> tuple[np.ndarray, np.ndarray]:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    pred = np.array([float(r["predicted"]) for r in rows])
    act = np.array([float(r["actual"]) for r in rows])
    ok = np.isfinite(pred) & np.isfinite(act)
    return pred[ok], act[ok]


def r2(pred: np.ndarray, act: np.ndarray) -> float:
    ss_res = float(np.sum((act - pred) ** 2))
    ss_tot = float(np.sum((act - act.mean()) ** 2))
    return 1.0 - ss_res / ss_tot


def shift_null(
    pred: np.ndarray, act: np.ndarray, observed: float, rng: np.random.Generator
) -> dict:
    """Circular-shift control: shifting the prediction keeps its autocorrelation.

    WHY not a plain permutation: speed series are strongly autocorrelated, so a permuted
    prediction loses temporal structure and gives an optimistic null.
    """
    n = pred.size
    lo, hi = SHIFT_MIN, n - SHIFT_MIN
    null = np.empty(N_SHIFT)
    for i in range(N_SHIFT):
        null[i] = r2(np.roll(pred, int(rng.integers(lo, hi))), act)
    sd = float(null.std(ddof=1))
    return {
        "null_mean": round(float(null.mean()), 4),
        "null_sd": round(sd, 4),
        "z": round((observed - float(null.mean())) / sd, 2) if sd > 0 else float("nan"),
        "shift_p": round(float((np.sum(null >= observed) + 1) / (N_SHIFT + 1)), 4),
    }


def block_boot_diff(
    pr: np.ndarray, pd: np.ndarray, act: np.ndarray, rng: np.random.Generator
) -> tuple[float, float, float]:
    """Circular-block bootstrap of r²(regressor) − r²(dummy) on the same frames."""
    n = act.size
    block = SHIFT_MIN
    n_blocks = int(np.ceil(n / block))
    diffs = np.empty(N_BOOT)
    for i in range(N_BOOT):
        starts = rng.integers(0, n, size=n_blocks)
        idx = (starts[:, None] + np.arange(block)[None, :]).ravel() % n
        idx = idx[:n]
        a = act[idx]
        diffs[i] = r2(pr[idx], a) - r2(pd[idx], a)
    lo, hi = np.quantile(diffs, [0.025, 0.975])
    return round(float(lo), 4), round(float(hi), 4), round(float(diffs.mean()), 4)


def analyse(root: Path, label: str, rng: np.random.Generator) -> tuple[list[dict], dict]:
    rows = []
    series: dict[tuple[str, int], dict[str, tuple[np.ndarray, np.ndarray]]] = {}
    for animal_dir in sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("sub-")):
        for test in sorted(animal_dir.glob("*_test.tsv")):
            model = "dummy" if "model-dummy" in test.name else "regressor"
            pred, act = read_pred_actual(test)
            value = r2(pred, act)
            row = {
                "set": label,
                "animal": animal_dir.name,
                "model": model,
                "file": test.name,
                "n_test": int(act.size),
                "r2": round(value, 4),
            }
            row.update(shift_null(pred, act, value, rng))
            rows.append(row)
            series.setdefault((animal_dir.name, int(act.size)), {})[model] = (pred, act)
    diffs = {}
    for key, pair in series.items():
        if "regressor" in pair and "dummy" in pair:
            pr, act = pair["regressor"][0], pair["regressor"][1]
            pd = pair["dummy"][0]
            diffs[key] = block_boot_diff(pr, pd, act, rng)
    return rows, diffs


def main() -> None:
    rng = np.random.default_rng(SEED)
    intra_rows, intra_diffs = analyse(DATA / "decode-speed", "intra", rng)
    inter_rows: list[dict] = []
    inter_diffs: dict = {}
    inter_root = DATA / "interanimal-decode-speed"
    if inter_root.exists():
        inter_rows, inter_diffs = analyse(inter_root, "inter", rng)

    intra_dummy_keys = {
        (r["animal"], r["n_test"], r["r2"]) for r in intra_rows if r["model"] == "dummy"
    }
    for r in inter_rows:
        if r["model"] == "dummy" and (r["animal"], r["n_test"], r["r2"]) in intra_dummy_keys:
            r["duplicate"] = True
    kept_inter = [r for r in inter_rows if not r.get("duplicate")]

    cols = ("set", "animal", "model", "n_test", "r2", "null_mean", "null_sd", "z", "shift_p")
    for r in intra_rows + inter_rows:
        flag = " DUPLICATE-VALUE" if r.get("duplicate") else ""
        print("\t".join(str(r[k]) for k in cols) + flag)

    for label, rows, diffs, paper_max in (
        ("intra", intra_rows, intra_diffs, PAPER_MAX_INTRA),
        ("inter", kept_inter, inter_diffs, PAPER_MAX_INTER),
    ):
        reg = [r["r2"] for r in rows if r["model"] == "regressor"]
        dum = [r["r2"] for r in rows if r["model"] == "dummy"]
        if reg:
            print(
                f"{label}: regressor max r2={max(reg):.4f} (paper quotes up to {paper_max}); "
                f"median={float(np.median(reg)):.4f}; n_files={len(reg)}"
            )
        if dum:
            print(
                f"{label}: dummy max r2={max(dum):.4f}; "
                f"median={float(np.median(dum)):.4f}; n_files={len(dum)}"
            )
        for key, (lo, hi, mean) in sorted(diffs.items()):
            print(
                f"{label}: diff regressor-dummy {key[0]} n={key[1]}: mean={mean} 95%CI=[{lo}, {hi}]"
            )


if __name__ == "__main__":
    main()
