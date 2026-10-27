"""H8 test (read-only): do delayed VolumeTiming intervals co-occur with wheel movement?

Uses only development-run wheel physio and VolumeTiming stamps. No fUS signal values are read,
and no causal conclusion is drawn.

For each onset interval [t_i, t_{i+1}) of a run:
  - TICK: interval in [0.299, 0.310] s;
  - DELAY: interval in (0.310, 0.450] s (delayed, not a gap);
  - gaps (> 0.450 s) are excluded, as in the frozen gap rule.
Activity of an interval: mean |wheel_velocity| over the physio samples in the interval (1000 Hz).

Observed statistic: mean over runs of (mean activity in DELAY − mean activity in TICK).
Reference: the wheel is shifted circularly within each recording by a random offset in
[-60, 60] s (200 draws, seed 20261029) while the stamps stay fixed. Two-sided p from the shifts.

Caveat: physio–VolumeTiming clock alignment is UNKNOWN, so any association is conditional on the
stamps being on the physio clock. No causal conclusion is drawn.
"""

from __future__ import annotations

import importlib.util
import json
import zipfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
EXP = REPO / "experiments" / "20261027-ne-exp-004-wheel-added-information-contract"
SEED = 20261029
N_SHIFTS = 200
SHIFT_MAX_S = 60.0
TICK_LO, TICK_HI = 0.299, 0.310
DELAY_HI = 0.450
FS = 1000.0


def load_controls():
    spec = importlib.util.spec_from_file_location(
        "controls", REPO / "scripts" / "run_nex001_controls.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_runs(C, dev: list[dict]) -> list[dict]:
    """Load stamps and the cumulative |wheel| once per run (the expensive step)."""
    zf = zipfile.ZipFile(C.ZIP)
    out = []
    for r in dev:
        base = f"sub-ALD002/fusi/{r['name']}"
        vt = np.array(json.loads(zf.read(base + "_pwd.json"))["VolumeTiming"], dtype=float)
        side, data = C._tsv(zf, base, "wheel")
        v = np.abs(data[:, side["Columns"].index("wheel_velocity")])
        # WHY doubled: a circular shift of the wheel within the recording needs windows that wrap.
        cum = np.concatenate([[0.0], np.cumsum(np.concatenate([v, v]))])
        out.append({"name": r["name"], "vt": vt, "cum": cum, "n": len(v), "duration": len(v) / FS})
    return out


def window_means(cum: np.ndarray, starts: np.ndarray, ends: np.ndarray) -> np.ndarray:
    lo = np.floor(starts * FS).astype(int)
    hi = np.floor(ends * FS).astype(int)
    return (cum[hi] - cum[lo]) / np.maximum(hi - lo, 1)


def run_diff(run: dict, vt: np.ndarray, shift: float = 0.0) -> tuple[float, float, float, int, int]:
    """Tick and delay activity with the wheel shifted circularly by `shift` s (0 = observed)."""
    dt = np.diff(vt)
    tick = (dt >= TICK_LO) & (dt <= TICK_HI)
    delay = (dt > TICK_HI) & (dt <= DELAY_HI)
    starts = (vt[:-1] + shift) % run["duration"]
    act = window_means(run["cum"], starts, starts + dt)
    a_t = float(act[tick].mean()) if tick.any() else np.nan
    a_d = float(act[delay].mean()) if delay.any() else np.nan
    return a_d - a_t, a_t, a_d, int(tick.sum()), int(delay.sum())


def main() -> None:
    C = load_controls()
    dev, _ = C.read_primary_runs()
    runs = load_runs(C, dev)
    rng = np.random.default_rng(SEED)
    shifts = rng.uniform(-SHIFT_MAX_S, SHIFT_MAX_S, size=N_SHIFTS)

    per_run = []
    for run in runs:
        obs, a_t, a_d, nt, nd = run_diff(run, run["vt"])
        null = []
        for s in shifts:
            null.append(run_diff(run, run["vt"], s)[0])
        null = np.array([x for x in null if np.isfinite(x)])
        p = float(2 * min(np.mean(null >= obs), np.mean(null <= obs))) if len(null) else np.nan
        per_run.append(
            {
                "run": run["name"],
                "n_tick": nt,
                "n_delay": nd,
                "mean_act_tick": round(a_t, 6),
                "mean_act_delay": round(a_d, 6),
                "diff_observed": round(obs, 6),
                "null_q025": round(float(np.quantile(null, 0.025)), 6),
                "null_q975": round(float(np.quantile(null, 0.975)), 6),
                "shift_draws_used": int(len(null)),
                "p_two_sided": round(p, 4),
            }
        )

    pooled_obs = float(np.mean([x["diff_observed"] for x in per_run]))
    pooled_null = []
    for s in shifts:
        vals = []
        for run in runs:
            vals.append(run_diff(run, run["vt"], s)[0])
        vals = np.array(vals)
        if np.all(np.isfinite(vals)):
            pooled_null.append(float(vals.mean()))
    pooled_null = np.array(pooled_null)
    pooled = {
        "statistic": "mean over runs of (DELAY mean − TICK mean of |wheel_velocity|)",
        "observed": round(pooled_obs, 6),
        "shift_draws_used": int(len(pooled_null)),
        "null_draws": [round(float(x), 8) for x in pooled_null],
        "null_q025": round(float(np.quantile(pooled_null, 0.025)), 6),
        "null_q975": round(float(np.quantile(pooled_null, 0.975)), 6),
        "p_two_sided": round(
            float(2 * min(np.mean(pooled_null >= pooled_obs), np.mean(pooled_null <= pooled_obs))),
            4,
        ),
    }
    out = {
        "question": "H8: do delayed VolumeTiming intervals co-occur with wheel movement?",
        "data": "development runs only; wheel_velocity and VolumeTiming stamps; no fUS values",
        "seed": SEED,
        "n_shifts_requested": N_SHIFTS,
        "shift_max_s": SHIFT_MAX_S,
        "tick_interval_s": [TICK_LO, TICK_HI],
        "delay_interval_s": [TICK_HI, DELAY_HI],
        "per_run": per_run,
        "pooled": pooled,
        "caveats": [
            "physio–VolumeTiming clock alignment is UNKNOWN; association is conditional on the "
            "stamps being on the physio clock",
            "circular shifts remove true alignment but keep the interval structure; a reference, "
            "not a causal test",
            "no causal conclusion; no fUS outcome used",
        ],
    }
    dest = EXP / "h8_delay_wheel.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("pooled", pooled)
    for x in per_run:
        print(
            x["run"],
            "tick",
            x["n_tick"],
            "delay",
            x["n_delay"],
            "obs",
            x["diff_observed"],
            "null",
            x["null_q025"],
            x["null_q975"],
            "p",
            x["p_two_sided"],
        )
    print("saved", dest)


if __name__ == "__main__":
    main()
