"""Paired comparison of CRT v1-config and v2 pilots, and the pre-registered verdict.

Reads crt_pilot_v1_n30.json, crt_pilot_v2_n30.json and crt_diagnostics.json from the NE-EXP-002
folder, writes crt_comparison.md. The decision rule is fixed in the approved plan and is applied
as written; it is not tuned to the results.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

FOLDER = Path("experiments/20261027-ne-exp-002-temporal-latent-confounding")
ALPHA = 0.05
NULL_SCENARIOS = ["zero_effect", "ar_null_strong", "measured_arousal"]
POWER_SCENARIO = "known_added_info"
Z95 = 1.959963984540054

_spec = importlib.util.spec_from_file_location(
    "pilot", Path(__file__).resolve().parent / "run_nex001_crt_pilot.py"
)
assert _spec is not None and _spec.loader is not None
_pilot_src = Path(__file__).resolve().parent / "run_nex001_crt_pilot.py"


def wilson(k: int, n: int) -> tuple[float, float]:
    p = k / n
    denom = 1 + Z95 * Z95 / n
    centre = (p + Z95 * Z95 / (2 * n)) / denom
    half = Z95 * np.sqrt(p * (1 - p) / n + Z95 * Z95 / (4 * n * n)) / denom
    return float(centre - half), float(centre + half)


def main() -> None:
    v1 = json.loads((FOLDER / "crt_pilot_v1_n30.json").read_text(encoding="utf-8"))
    v2 = json.loads((FOLDER / "crt_pilot_v2_n30.json").read_text(encoding="utf-8"))
    diag = json.loads((FOLDER / "crt_diagnostics.json").read_text(encoding="utf-8"))
    n = v2["n_reps"]
    assert v1["n_reps"] == n and v1["n_draws"] == v2["n_draws"]

    lines = [
        "# CRT pilot comparison: v1 configuration vs v2 (NE-EXP-002, synthetic only)",
        "",
        f"v1-config code_version: `{v1['code_version']}` flags {v1['flags']}  ",
        f"v2 code_version: `{v2['code_version']}` flags {v2['flags']}  ",
        f"reps per scenario: {n}, draws per replicate: {v2['n_draws']}, alpha {ALPHA}, "
        f"same seed {v2['seed']} (paired synthetic series)",
        "",
        "## Rejection rates (conditional test, and the independent comparator)",
        "",
        "| scenario | kind | v1-config k/n | v1 Wilson95 | v2 k/n | v2 Wilson95 "
        "| paired b (v1 only) | paired c (v2 only) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    verdict_flags = []
    power_ok = None
    power_v1 = power_v2 = None
    for scen in v2["results"]:
        for kind in ("independent", "conditional"):
            k1 = v1["results"][scen][kind]["rejections"]
            k2 = v2["results"][scen][kind]["rejections"]
            p1 = np.array(v1["results"][scen]["p_values"][kind])
            p2 = np.array(v2["results"][scen]["p_values"][kind])
            r1 = p1 <= ALPHA
            r2 = p2 <= ALPHA
            b = int(np.sum(r1 & ~r2))
            c = int(np.sum(~r1 & r2))
            w1 = wilson(k1, n)
            w2 = wilson(k2, n)
            lines.append(
                f"| {scen} | {kind} | {k1}/{n} | [{w1[0]:.3f}, {w1[1]:.3f}] | {k2}/{n} | "
                f"[{w2[0]:.3f}, {w2[1]:.3f}] | {b} | {c} |"
            )
            if kind == "conditional" and scen in NULL_SCENARIOS and k2 >= 7 and w2[0] > 0.10:
                verdict_flags.append(f"{scen}: v2 conditional {k2}/{n}, Wilson lower {w2[0]:.3f}")
            if kind == "conditional" and scen == POWER_SCENARIO:
                power_v1, power_v2 = k1 / n, k2 / n
                power_ok = (k2 / n >= 0.5) and (k1 / n - k2 / n <= 0.10)

    lines += [
        "",
        "Paired differences in rejection rate (v2 minus v1-config) equal (c - b) / n.",
        "",
        "## Mean p-value and mean 95% null quantile",
        "",
        "| scenario | kind | v1 mean p | v2 mean p | v1 mean q95 null | v2 mean q95 null |",
        "|---|---|---|---|---|---|",
    ]
    for scen in v2["results"]:
        for kind in ("independent", "conditional"):
            a = v1["results"][scen][kind]
            b2 = v2["results"][scen][kind]
            lines.append(
                f"| {scen} | {kind} | {a['mean_p']:.3f} | {b2['mean_p']:.3f} | "
                f"{a['mean_q95_null']:.6f} | {b2['mean_q95_null']:.6f} |"
            )

    qr = diag["summary"]["quarter_var_ratio_std"]["median"]
    diag_fail = []
    if qr > 1.5:
        diag_fail.append(f"quarter variance ratio after standardisation median {qr} > 1.5")
    if diag["summary"]["block_var_ratio_max_min"]["median"] > 3.0:
        diag_fail.append(
            "block variance ratio (max/min across blocks) median "
            f"{diag['summary']['block_var_ratio_max_min']['median']} > 3"
        )

    if verdict_flags:
        verdict = "BLOCKED"
        reason = "null inflation flagged: " + "; ".join(verdict_flags)
    elif diag_fail:
        verdict = "REVISE"
        reason = "no null flag, but diagnostics fail: " + "; ".join(diag_fail)
    elif power_ok:
        verdict = "PROCEED"
        reason = "no null flag, power retained, diagnostics pass"
    else:
        verdict = "REVISE"
        reason = f"power check failed (v1 {power_v1:.2f}, v2 {power_v2:.2f})"

    lines += [
        "",
        "## Pre-registered decision",
        "",
        f"- Null inflation flags: {verdict_flags or 'none'}",
        f"- Power (known_added_info): v1 {power_v1}, v2 {power_v2}, retained: {power_ok}",
        f"- Diagnostics failing: {diag_fail or 'none'}",
        "",
        f"**Verdict: {verdict}.** {reason}.",
        "",
        "Caveats: n = 30 replicates per scenario; Wilson intervals are wide; the diagnostics use a "
        "pooled OLS mu (diagnostic only); the conditional test is approximate, not an exact CRT.",
    ]
    out = FOLDER / "crt_comparison.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("verdict", verdict, "-", reason)
    print("saved", out)


if __name__ == "__main__":
    main()
