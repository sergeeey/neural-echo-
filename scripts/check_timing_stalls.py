"""Read-only test of the sporadic-delay model of VolumeTiming (no fUS values).

Model under test (H-stall): onsets are ticks of an exact 0.300 s clock, delayed sporadically. Then
intervals are 0.300 s, or 0.300 s plus a positive delay, and the excess over 0.300 s is one-sided.

For each eligible run, reports:
  - the minimum and median non-gap interval;
  - the share of non-gap intervals at exactly the median and above it (one-sided check);
  - histogram counts above 0.301 s in bins (0.301-0.31, 0.31-0.35, 0.35-0.45 s);
  - the total delay budget: sum of (interval - 0.300) over non-gap intervals, plus the sum over gap
    intervals of (interval - round(interval/0.300) x 0.300); this equals the endpoint excess under
    the 0.300 s model.
Exploratory: the delay model is an inference to be tested, not a result.
"""

from __future__ import annotations

import importlib.util
import json
import zipfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
EXP = REPO / "experiments" / "20261027-ne-exp-004-wheel-added-information-contract"
TICK = 0.300
GAP_S = 0.45


def load_controls():
    spec = importlib.util.spec_from_file_location(
        "controls", REPO / "scripts" / "run_nex001_controls.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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
        gaps = dt[dt > GAP_S]
        med = float(np.median(normal))
        excess_normal = float(np.sum(normal - TICK))
        gap_resid = float(np.sum(gaps - np.rint(gaps / TICK) * TICK))
        rows.append(
            {
                "run": r["name"],
                "n_nongap": int(len(normal)),
                "min_nongap_s": float(normal.min()),
                "median_nongap_s": med,
                "share_at_median": float(np.mean(np.isclose(normal, med, atol=1e-9))),
                "share_below_median": float(np.mean(normal < med - 1e-9)),
                "n_0p301_0p31": int(np.sum((normal > 0.301) & (normal <= 0.31))),
                "n_0p31_0p35": int(np.sum((normal > 0.31) & (normal <= 0.35))),
                "n_0p35_0p45": int(np.sum((normal > 0.35) & (normal <= 0.45))),
                "delay_budget_nongap_s": round(excess_normal, 4),
                "gap_residual_sum_s": round(gap_resid, 4),
                "delay_budget_total_s": round(excess_normal + gap_resid, 4),
            }
        )
    dest = EXP / "timing_stalls.json"
    dest.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for x in rows:
        print(
            x["run"],
            "min",
            round(x["min_nongap_s"], 4),
            "median",
            round(x["median_nongap_s"], 4),
            "below-median share",
            round(x["share_below_median"], 4),
            "(0.301-0.31, 0.31-0.35, 0.35-0.45):",
            x["n_0p301_0p31"],
            x["n_0p31_0p35"],
            x["n_0p35_0p45"],
            "budget",
            x["delay_budget_total_s"],
        )
    print("saved", dest)


if __name__ == "__main__":
    main()
