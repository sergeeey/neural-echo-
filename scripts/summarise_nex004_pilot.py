"""Summary tables for the NE-EXP-004 diagnostic pilot.

Reads pilot_results.json and writes pilot_summary.md in the contract folder. It performs no new
computation on the data: per held-out date, the C1 check for each statistic, the rest / movement /
transition diagnostics, the oracle C6 values (descriptive), and the C3-B outcome with its binomial
reading. Intervals: Wilson 95% for K over 60 replicates.
"""

from __future__ import annotations

import json
from math import comb, sqrt
from pathlib import Path

EXP = Path("experiments/20261027-ne-exp-004-wheel-added-information-contract")
Z95 = 1.959963984540054
RIGHT_ARROW = "—"


def wilson(k: int, n: int) -> tuple[float, float]:
    p = k / n
    denom = 1 + Z95 * Z95 / n
    centre = (p + Z95 * Z95 / (2 * n)) / denom
    half = Z95 * sqrt(p * (1 - p) / n + Z95 * Z95 / (4 * n * n)) / denom
    return centre - half, centre + half


def c1_lines(A: dict) -> list[str]:
    lines = [
        "## Block A — candidate A, contract C1 (training-only generator, nested out-of-sample)",
        "",
        "Criterion per statistic T and training date j: |O_j − m_j| ≤ 2 s_T, where s_T is the SD",
        "of the observed values across the five training dates of that held-out fold.",
        "",
        "| held-out d | admissible | failing (date, statistic): O, m, limit |",
        "|---|---|---|",
    ]
    for d, ok in A["admissible"].items():
        fails = []
        for j, checks in A["per_date"][d]["checks"].items():
            for t, c in checks.items():
                if not c["pass"]:
                    fails.append(
                        f"({j}, {t}): O={c['OBS']:.4g}, m={c['m']:.4g}, limit={c['limit_2s']:.4g}"
                    )
        lines.append(f"| {d} | {ok} | {'; '.join(fails) if fails else RIGHT_ARROW} |")
    return lines


def diagnostic_lines(A: dict) -> list[str]:
    lines = [
        "## Block A — rest / movement / transition diagnostics (per scored training date)",
        "",
        "Held-out fold d is left out; each row is a scored training date j, fitted on the other",
        "dates (out-of-sample).",
        "",
        "| d | j | p01 obs / fit / sur | p10 obs / fit / sur "
        "| rest q50 obs / sur "
        "| active q50 obs / sur | amp q50 obs / sur |",
        "|---|---|---|---|---|---|---|",
    ]
    for d, block in A["per_date"].items():
        for j, g in block["diagnostics"].items():
            ot = g["obs_p01_p10"]
            p01 = f"{ot[0]:.3f} / {g['p01_fit']:.3f} / {g['sur_p01_median']:.3f}"
            p10 = f"{ot[1]:.3f} / {g['p10_fit']:.3f} / {g['sur_p10_median']:.3f}"
            rest = f"{g['obs_rest_len_q50_q90'][0]:.0f} / {g['sur_rest_len_q50_median']:.0f}"
            act = f"{g['obs_act_len_q50_q90'][0]:.0f} / {g['sur_act_len_q50_median']:.0f}"
            amp = f"{g['obs_amp_q05_q50_q95'][1]:.3f} / {g['sur_amp_q50_median'][1]:.3f}"
            lines.append(f"| {d} | {j} | {p01} | {p10} | {rest} | {act} | {amp} |")
    return lines


def oracle_lines(A: dict) -> list[str]:
    lines = [
        "## Block A — oracle C6 (held-out wheel statistics; descriptive;",
        "cannot change admissibility)",
        "",
        "| d | S1 z | S3 z | S4 z | S5 z | S6 z |",
        "|---|---|---|---|---|---|",
    ]
    for d, z in A.get("oracle_C6", {}).items():
        cells = []
        for t in ("S1", "S3", "S4", "S5", "S6"):
            v = z[t]["z"]
            cells.append(RIGHT_ARROW if v is None else f"{v:+.2f}")
        lines.append(f"| {d} | " + " | ".join(cells) + " |")
    return lines


def block_b_lines(B: dict) -> list[str]:
    k = B["K"]
    n = B["replicates_done"]
    lo, hi = wilson(k, n)
    p_flag_05 = sum(comb(60, i) * 0.05**i * 0.95 ** (60 - i) for i in range(8, 61))
    return [
        "## Block B — candidate B, C3-B (60 zero-effect replicates)",
        "",
        f"K = {k} of {n} replicates declared support (pooled Δ > 0 and bootstrap lower bound > 0).",
        f"Wilson 95% interval for the rate K/n: [{lo:.3f}, {hi:.3f}].",
        f"Outcome under the fixed rule (K ≥ 8 flags): **{B['outcome']}**.",
        "This outcome is NOT a demonstration of calibration. For reference, a rule of true size",
        f"0.05 is flagged with probability {p_flag_05:.4f} (exact binomial, 60 replicates).",
    ]


def main() -> None:
    res = json.loads((EXP / "pilot_results.json").read_text(encoding="utf-8"))
    A = res["A"]
    B = res["B"]
    head = [
        "# NE-EXP-004 diagnostic pilot: summary",
        "",
        f"Code: `{A['code']}`. Seed {A['seed']} (block A); seeds "
        f"{B['seed_synth']} / {B['seed_bootstrap']} (block B).",
        f"CPU used: {res['cpu_hours_total']} CPU-hours of a 0.3 budget (process time).",
        "",
    ]
    lines = head + c1_lines(A) + [""] + diagnostic_lines(A) + [""] + oracle_lines(A) + [""]
    lines += block_b_lines(B)
    out = EXP / "pilot_summary.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("saved", out)


if __name__ == "__main__":
    main()
