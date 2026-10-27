"""Read-only structural timing checks for NE-EXP-004 Phase B (development runs; no fUS values).

For each eligible development run: VolumeTiming length, onset spacing and the drift implied by the
frame period quoted in docs/STATUS.md, gap count, first and last onset, physio duration and
sampling, whether the physio recording covers the onsets, and how many aligned wheel frames remain
after the coverage trim. These are the pre-run checks C-V1 to C-V3 of the Phase B protocol. A
discrepancy is reported as a number and is never hidden by a tolerance.
"""

from __future__ import annotations

import importlib.util
import json
import zipfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
EXP = REPO / "experiments" / "20261027-ne-exp-004-wheel-added-information-contract"
QUOTED_PERIOD = 0.30013  # frame period quoted in docs/STATUS.md
TOL_V2_S = 0.1  # one third of a frame; fixed before the corrected C-V2 statistic was computed
GAP_S = 0.45  # same gap threshold as the primary analysis


def load_controls():
    spec = importlib.util.spec_from_file_location(
        "controls", REPO / "scripts" / "run_nex001_controls.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_row(C, zf, r: dict) -> dict:
    base = f"sub-ALD002/fusi/{r['name']}"
    vt = np.array(json.loads(zf.read(base + "_pwd.json"))["VolumeTiming"], dtype=float)
    dt = np.diff(vt)
    side, data = C._tsv(zf, base, "wheel")
    fs = float(side["SamplingFrequency"])
    physio_dur = len(data) / fs
    return {
        "run": r["name"],
        "date": r["date"],
        "vt_len": int(len(vt)),
        "vt_first_s": float(vt[0]),
        "vt_last_s": float(vt[-1]),
        "dt_median_s": float(np.median(dt)),
        "dt_min_s": float(dt.min()),
        "dt_max_s": float(dt.max()),
        # Endpoint discrepancy: onset span minus the excess of gap intervals, minus the span
        # expected from the quoted period. WHY span-based: the median of quantised intervals
        # (about 1 ms steps) gave a spurious drift; see the record of C-V2 correction.
        "drift_s": float(
            (vt[-1] - vt[0] - np.sum(dt[dt > GAP_S] - QUOTED_PERIOD))
            - (len(vt) - 1) * QUOTED_PERIOD
        ),
        "median_dt_s": float(np.median(dt)),
        "gaps": int(np.sum(dt > GAP_S)),
        "physio_fs": fs,
        "physio_dur_s": float(physio_dur),
        "covers": bool(physio_dur >= vt[-1] + 0.3),
        "wheel_frames": int(len(r["wheel"])),
    }


def table(rows: list[dict]) -> list[str]:
    head = [
        "| run | date | VT len | VT first–last (s) | dt median / min / max (s) "
        "| endpoint discrepancy, gap excess removed (s) | gaps >0.45 s | physio fs / dur (s) "
        "| physio covers | aligned wheel frames |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    body = []
    for x in rows:
        span = f"{x['vt_first_s']:.1f}–{x['vt_last_s']:.1f}"
        dts = f"{x['dt_median_s']:.5f} / {x['dt_min_s']:.5f} / {x['dt_max_s']:.5f}"
        phys = f"{x['physio_fs']:.1f} / {x['physio_dur_s']:.1f}"
        body.append(
            f"| {x['run']} | {x['date']} | {x['vt_len']} | {span} | {dts} "
            f"| {x['drift_s']:+.2f} | {x['gaps']} | {phys} | {x['covers']} "
            f"| {x['wheel_frames']} |"
        )
    return head + body


def main() -> None:
    C = load_controls()
    dev, excluded = C.read_primary_runs()
    zf = zipfile.ZipFile(C.ZIP)
    rows = [run_row(C, zf, r) for r in dev]
    drifts = [x["drift_s"] for x in rows]
    v2_pass = bool(max(abs(d) for d in drifts) <= TOL_V2_S)
    n_cov = sum(x["covers"] for x in rows)
    excl = ", ".join(excluded) if excluded else "none"
    lines = [
        "# Phase B structural timing checks (development runs; read-only)",
        "",
        f"Eligible runs: {len(rows)}. Excluded for count mismatch: {len(excluded)} ({excl}).",
        "The holdout is excluded by name and is not read.",
        "",
    ]
    lines += table(rows)
    lines += [
        "",
        f"C-V1 (VolumeTiming length equals frame count): enforced by read_primary_runs; "
        f"{len(rows)} of {len(rows)} eligible.",
        f"C-V2 (endpoint discrepancy with the quoted period {QUOTED_PERIOD} s, gap excess removed, "
        f"tolerance {TOL_V2_S} s, fixed before this statistic was computed): "
        f"{'PASSED' if v2_pass else 'NOT PASSED'}. Range over runs {min(drifts):+.3f} s to "
        f"{max(drifts):+.3f} s.",
        "Correction record: an earlier version used the median onset interval and reported",
        "a drift of −1.08 to −1.47 s. The median is not the mean period (onsets are quantised",
        "to 1 ms and gaps skew the mean), so that statistic over-states the drift; withdrawn.",
        "The corrected endpoint discrepancy is at least about 0.5 s in some runs (largest with",
        "long gaps). The physio-fUS clock offset and the onset-versus-end convention are",
        "unquantified; they are not measured by this check.",
        f"C-V3 (physio recording covers all onsets): {n_cov} of {len(rows)} runs.",
        "",
        "Not checked here: the VolumeTiming convention (onset relative to frame start or end) and",
        "the clock alignment between physio and fUS. Both remain open; temporal interpretation is",
        "not permitted until they are resolved.",
    ]
    out = EXP / "phase_b_timing_checks.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("saved", out)


if __name__ == "__main__":
    main()
