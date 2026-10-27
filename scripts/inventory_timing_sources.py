"""Read-only inventory of timing sources for the eligible development runs (no fUS values).

For each run: the sidecar fields that carry timing (RepetitionTime, FrameAcquisitionDuration,
SliceTiming if present, VolumeTiming summary), the NIfTI header pixdim[4] (frame period as stored),
the number of frames in the header, the physio sidecar StartTime and sampling rate, and the spacing
statistics of VolumeTiming. Used only to locate which source carries which value.
"""

from __future__ import annotations

import importlib.util
import json
import struct
import zipfile
import zlib
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
EXP = REPO / "experiments" / "20261027-ne-exp-004-wheel-added-information-contract"


def load_controls():
    spec = importlib.util.spec_from_file_location(
        "controls", REPO / "scripts" / "run_nex001_controls.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def nifti_header(zf: zipfile.ZipFile, base: str) -> dict:
    head = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(zf.read(base + "_pwd.nii.gz"), 352)
    dims = struct.unpack("<8h", head[40:56])
    pixdim = struct.unpack("<8f", head[76:108])
    return {"dim": list(dims), "pixdim": [round(float(p), 6) for p in pixdim]}


def main() -> None:
    C = load_controls()
    dev, excluded = C.read_primary_runs()
    zf = zipfile.ZipFile(C.ZIP)
    out = []
    for r in dev:
        base = f"sub-ALD002/fusi/{r['name']}"
        side = json.loads(zf.read(base + "_pwd.json"))
        vt = np.array(side["VolumeTiming"], dtype=float)
        dt = np.diff(vt)
        nh = nifti_header(zf, base)
        keys = {k: side[k] for k in side if k != "VolumeTiming"}
        psd = json.loads(zf.read(base + "_recording-wheel_physio.json"))
        out.append(
            {
                "run": r["name"],
                "date": r["date"],
                "sidecar_scalars": {
                    k: v for k, v in keys.items() if not isinstance(v, (list, dict))
                },
                "sidecar_nonscalar_keys": sorted(
                    k for k, v in keys.items() if isinstance(v, (list, dict))
                ),
                "nifti_dim": nh["dim"],
                "nifti_pixdim": nh["pixdim"],
                "vt_len": int(len(vt)),
                "vt_mean_period": float((vt[-1] - vt[0]) / (len(vt) - 1)),
                "vt_median_dt": float(np.median(dt)),
                "vt_intervals_within_0p2_0p4": int(np.sum((dt > 0.2) & (dt < 0.4))),
                "physio_start": psd.get("StartTime"),
                "physio_fs": psd.get("SamplingFrequency"),
            }
        )
    lines = [json.dumps(out, indent=2, ensure_ascii=False)]
    dest = EXP / "timing_sources_inventory.json"
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("saved", dest, "excluded:", len(excluded))
    for x in out:
        print(
            x["run"],
            "nifti pixdim4=",
            x["nifti_pixdim"][4],
            "vt mean=",
            round(x["vt_mean_period"], 6),
            "vt median=",
            round(x["vt_median_dt"], 6),
            "sidecar scalars=",
            x["sidecar_scalars"],
        )


if __name__ == "__main__":
    main()
