"""Read-only lattice analysis of VolumeTiming for the eligible development runs (no fUS values).

Question: are the onset intervals consistent with one frame period plus whole missed volumes?
For each run:
  - period estimates from non-gap intervals (mean and median);
  - for each gap interval (above 0.45 s): the nearest integer number of periods k and the residual;
  - the lattice residual: span minus the span implied by (n - 1 + missing volumes) x period;
  - the same residual with two candidate periods: 0.3 s (sidecar FrameAcquisitionDuration)
    and 0.30013 s (value quoted in docs/STATUS.md).
This is an exploratory inspection to inform the proposed amendment. The admission rule is stated in
the amendment and is not tuned to these numbers.
"""

from __future__ import annotations

import importlib.util
import json
import zipfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
EXP = REPO / "experiments" / "20261027-ne-exp-004-wheel-added-information-contract"
GAP_S = 0.45
CANDIDATES = {"sidecar_0.3": 0.3, "quoted_0.30013": 0.30013}


def load_controls():
    spec = importlib.util.spec_from_file_location(
        "controls", REPO / "scripts" / "run_nex001_controls.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lattice_residual(vt: np.ndarray, period: float) -> tuple[float, int, float]:
    dt = np.diff(vt)
    gaps = dt > GAP_S
    k = np.rint(dt[gaps] / period)
    missing = int(np.sum(k - 1))
    implied = (len(vt) - 1 + missing) * period
    span = vt[-1] - vt[0]
    max_gap_resid = float(np.max(np.abs(dt[gaps] - k * period))) if gaps.any() else 0.0
    return float(span - implied), missing, max_gap_resid


def main() -> None:
    C = load_controls()
    dev, _ = C.read_primary_runs()
    zf = zipfile.ZipFile(C.ZIP)
    rows = []
    for r in dev:
        base = f"sub-ALD002/fusi/{r['name']}"
        vt = np.array(json.loads(zf.read(base + "_pwd.json"))["VolumeTiming"], dtype=float)
        dt = np.diff(vt)
        normal = dt[dt <= GAP_S]
        row = {
            "run": r["name"],
            "n": int(len(vt)),
            "gaps": int(np.sum(dt > GAP_S)),
            "period_mean_nongap": float(normal.mean()),
            "period_median_nongap": float(np.median(normal)),
            "period_sd_nongap_ms": float(normal.std() * 1000),
        }
        per_run = {**CANDIDATES, "per_run_mean_nongap": float(normal.mean())}
        for label, p in per_run.items():
            res, missing, gmax = lattice_residual(vt, p)
            row[f"lattice_resid_{label}_s"] = round(res, 4)
            row[f"missing_{label}"] = missing
            row[f"max_gap_resid_{label}_s"] = round(gmax, 4)
        row["gap_intervals_s"] = [round(float(x), 4) for x in dt[dt > GAP_S]]
        rows.append(row)
    dest = EXP / "timing_lattice.json"
    dest.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for x in rows:
        print(
            x["run"],
            "n",
            x["n"],
            "gaps",
            x["gaps"],
            "period mean/median",
            round(x["period_mean_nongap"], 6),
            round(x["period_median_nongap"], 6),
            "sd ms",
            round(x["period_sd_nongap_ms"], 3),
            "| 0.3:",
            x["lattice_resid_sidecar_0.3_s"],
            "missing",
            x["missing_sidecar_0.3"],
            "| 0.30013:",
            x["lattice_resid_quoted_0.30013_s"],
            "missing",
            x["missing_quoted_0.30013"],
        )
    print("saved", dest)


if __name__ == "__main__":
    main()
