"""Check that v1-config and v2 consume the same random stream, so their synthetic series match.

Runs one replicate per scenario for each version, with the same loop order the pilot uses,
and compares a digest of every synthetic outcome series plus the final RNG state.
"""

import hashlib
import importlib.util
import sys
from pathlib import Path

import numpy as np

REPO = Path("E:/РАБОИЕ ПРОЕКТЫ👌/A-9  Neural Echo")
sys.argv = ["pilot", "1", "19", "2"]  # import-time argv only; loop below is explicit
spec = importlib.util.spec_from_file_location("pilot", REPO / "scripts" / "run_nex001_crt_pilot.py")
assert spec is not None and spec.loader is not None
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

from neural_echo.crt import build_plans, run_test  # noqa: E402

dev, _ = P.C.read_primary_runs()
N_DRAWS = 19


def digest(arrs: list[np.ndarray]) -> str:
    h = hashlib.sha256()
    for a in arrs:
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()[:16]


out = {}
for version, flags in (
    (1, {"standardise": False, "edge_frames": 20}),
    (2, {"standardise": True, "edge_frames": 40}),
):
    rng = np.random.default_rng(P.SEED)
    rows = []
    for name in P.SCENARIOS:
        runs, _ = P.synth(name, dev, rng)
        plans = build_plans(runs, conditional=True, **flags)
        for cond in (False, True):
            run_test(plans, runs, N_DRAWS, rng, conditional=cond)
        rows.append((name, digest([r.y for r in runs]), digest([r.wheel for r in runs])))
    out[version] = (rows, rng.bit_generator.state["state"]["state"])

same_y = all(a[1] == b[1] and a[2] == b[2] for a, b in zip(out[1][0], out[2][0], strict=True))
same_state = out[1][1] == out[2][1]
for a, b in zip(out[1][0], out[2][0], strict=True):
    print(a[0], "y v1", a[1], "v2", b[1], "| wheel v1", a[2], "v2", b[2], "match", a[1] == b[1])
print("all synthetic series identical:", same_y)
print("final RNG state identical:", same_state)
