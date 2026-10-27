"""Protocol C4: sync check between running speed and the fUS global signal (descriptive).

For each session, the lag (in fUS volumes) of maximum absolute cross-correlation between the
speed series (interpolated to VolumeTiming) and the mean fUS signal over selected voxels is
reported. Descriptive only: nothing is fitted or selected on it. The protocol asks that a lag
far from the expected haemodynamic range (0 to 3 s) is read as a red flag.

Reads the same files as scripts/run_cybis_speed_baseline.py and reuses its loaders.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw" / "cybis_pereira_2026"
ANIMAL = "sub-rat1703"
SESSIONS = ["ses-20210407", "ses-20210412", "ses-20210421"]
MAX_LAG = 10  # volumes; about 6 s at 0.6 s per volume
OUT = REPO / "docs" / "results" / "cybis_speed_sync.json"


def _load_baseline():
    path = REPO / "scripts" / "run_cybis_speed_baseline.py"
    spec = importlib.util.spec_from_file_location("baseline", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def xcorr(a: np.ndarray, b: np.ndarray, max_lag: int) -> dict[int, float]:
    """Pearson r between a[t] and b[t + lag] for lag in [-max_lag, max_lag]."""
    out = {}
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            x, y = a[: a.size - lag], b[lag:]
        else:
            x, y = a[-lag:], b[: b.size + lag]
        out[lag] = float(np.corrcoef(x, y)[0, 1])
    return out


def main() -> None:
    B = _load_baseline()
    results = {"animal": ANIMAL, "max_lag_volumes": MAX_LAG, "sessions": []}
    for s in SESSIONS:
        fus_dir = RAW / "rawdata" / ANIMAL / s / "fus"
        js = json.loads(
            (fus_dir / f"{ANIMAL}_{s}_task-openfield_pwd.json").read_text(encoding="utf-8")
        )
        vt = np.array(js["VolumeTiming"], dtype=float)
        vol, _ = B.read_nifti(fus_dir / f"{ANIMAL}_{s}_task-openfield_pwd.nii.gz")
        T = vol.shape[-1]
        flat = vol.reshape(-1, T)
        ok = np.isfinite(flat).all(axis=1) & (flat.std(axis=1) > 0)
        X = flat[ok].T
        glob = ((X - X.mean(axis=0)) / X.std(axis=0)).mean(axis=1)  # mean of per-voxel z
        speed = B.load_speed(
            RAW
            / "rawdata"
            / ANIMAL
            / s
            / "motion"
            / f"{ANIMAL}_{s}_task-openfield_tracksys-DLC_motion.tsv",
            vt,
        )
        xc = xcorr(speed, glob, MAX_LAG)
        best = max(xc, key=lambda k: abs(xc[k]))
        results["sessions"].append(
            {
                "session": s,
                "n_frames": int(T),
                "n_voxels_used": int(ok.sum()),
                "best_lag_volumes": best,
                "best_lag_s": round(best * float(np.median(np.diff(vt))), 3),
                "best_r": round(xc[best], 4),
                "r_at_lag0": round(xc[0], 4),
                "xcorr": {str(k): round(v, 4) for k, v in xc.items()},
            }
        )
        print(
            s,
            "best_lag_volumes",
            best,
            "best_r",
            round(xc[best], 4),
            "r0",
            round(xc[0], 4),
            flush=True,
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("saved", OUT.name)


if __name__ == "__main__":
    main()
