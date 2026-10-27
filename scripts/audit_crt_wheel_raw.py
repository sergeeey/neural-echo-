"""Read-only audit of the raw wheel physio channel for the eligible development runs.

Question: are the exact zeros in the wheel frames a property of the recording (stationary wheel
samples) or of the processing (fill values, clipping, missing data)?
"""

import importlib.util
import json
import zipfile
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location(
    "controls", Path("E:/РАБОИЕ ПРОЕКТЫ👌/A-9  Neural Echo/scripts/run_nex001_controls.py")
)
assert spec is not None and spec.loader is not None
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

zf = zipfile.ZipFile(C.ZIP)
names = sorted(
    n.rsplit("/", 1)[-1].replace("_pwd.json", "")
    for n in zf.namelist()
    if n.startswith("sub-ALD002/fusi/") and n.endswith("_pwd.json")
)
dev_names = [n for n in names if n != C.HOLDOUT]
print("sidecar wheel description and units (first run):")
first = f"sub-ALD002/fusi/{dev_names[0]}"
side_all = json.loads(zf.read(f"{first}_recording-wheel_physio.json"))
print({k: v for k, v in side_all.items() if k != "Columns"}, side_all.get("Columns"))

print("\nper-run raw wheel_velocity statistics (all samples, before windowing):")
for name in dev_names:
    base = f"sub-ALD002/fusi/{name}"
    side, data = C._tsv(zf, base, "wheel")
    col = data[:, side["Columns"].index("wheel_velocity")]
    zero = col == 0
    nan = ~np.isfinite(col)
    # run lengths of consecutive exact zeros
    d = np.diff(np.concatenate([[0], zero.astype(int), [0]]))
    lens = np.where(d == -1)[0] - np.where(d == 1)[0]
    fs = side["SamplingFrequency"]
    win = int(round(0.3 * fs))
    win_zero = np.array([zero[i : i + win].all() for i in range(0, len(col) - win, win)])
    print(
        f"{name} n={len(col)} fs={fs} exact_zero={zero.mean():.3f} nan={nan.sum()} "
        f"zero_runs={len(lens)} median_zero_run_samples={np.median(lens) if len(lens) else 0:.0f} "
        f"max_zero_run_s={lens.max() / fs if len(lens) else 0:.2f} "
        f"frac_0.3s_windows_all_zero={win_zero.mean():.3f} "
        f"min={np.nanmin(col):.4g} max={np.nanmax(col):.4g} "
        f"neg_frac={np.mean(col < 0):.3f} distinct={len(np.unique(col))}"
    )
