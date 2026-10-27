"""Summarise NE-EXP-001 synthetic controls as a PRELIMINARY, EXPLORATORY record.

Reads controls_results.json and writes synthetic_controls_preliminary.md with Wilson 95% intervals
for each detection rate, plus the code version and run settings. No new simulation is run here.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

EXP = Path("experiments/20261026-ne-exp-001-fusi-measurement-ceiling")
Z = 1.959963984540054

ROLE = {
    "zero_effect": "null: no effect (false positives)",
    "ar_null_strong": "null: strong autocorrelation (false positives)",
    "eye_driven": "null: signal driven by measured eye (nuisance adequacy)",
    "known_effect": "power: wheel effect, R² 0.05 in truth (optimistic kernel)",
    "delayed_outside": "wheel effect delayed 6 s (timing specificity)",
    "lead_misalignment": "wheel effect advanced 2.1 s (timing direction)",
    "hidden_confound": "unmeasured arousal correlated with wheel (wheel-specificity)",
}


def wilson(k: int, n: int) -> tuple[float, float]:
    """Wilson score interval for k successes out of n."""
    p = k / n
    denom = 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / denom
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / denom
    return centre - half, centre + half


def commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()


def header(data: dict) -> list[str]:
    return [
        "# Synthetic controls for NE-EXP-001: PRELIMINARY (EXPLORATORY)",
        "",
        "Status: **preliminary**. Simulation results on development-run inputs with known truth.",
        "They are not evidence about the real signal and are not a basis for any freeze.",
        "",
        "## Provenance",
        "",
        f"- Code version: git commit {commit()} (`scripts/run_nex001_controls.py`, "
        "primitives in `src/neural_echo/exp001.py`).",
        f"- Seed: {data['seed']} (single `numpy.random.default_rng`, fixed scenario order).",
        f"- Data: {data['data']}.",
        f"- Primary runs: {len(data['primary_runs'])}; dates: {len(data['primary_dates'])}; "
        f"excluded mismatched runs: {len(data['excluded_mismatched'])}.",
        f"- Consistency rule: {data['consistency_rule']}.",
        f"- Mean wheel–eye correlation over primary runs (zero lag): "
        f"{data['mean_wheel_eye_correlation']}.",
    ]


def table(data: dict) -> list[str]:
    rows = [
        "| Scenario | Role | Count | Rate | Wilson 95% | Margin-only (Wilson 95%) | Perms |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, res in data["results"].items():
        n = res["n_replicates"]
        k = round(res["detection_rate_full_rule"] * n)
        lo, hi = wilson(k, n)
        km = round(res["detection_rate_margin_only"] * n)
        mlo, mhi = wilson(km, n)
        rows.append(
            f"| {name} | {ROLE[name]} | {k}/{n} | {k / n:.3f} | [{lo:.3f}, {hi:.3f}] | "
            f"[{mlo:.3f}, {mhi:.3f}] | {res['n_permutations']} |"
        )
    return rows


READING = [
    "## Reading (what this does and does not show)",
    "",
    "- Null rows bound the false-positive rate of the full rule at this precision. With 40",
    "  replicates, values up to about 0.12 are compatible with the nominal 0.05. Precision is",
    "  too low to certify calibration.",
    "- Positive and stress rows show what the design detects. They do not show that the detected",
    "  effect is wheel-specific, temporal, or neural: hidden_confound, delayed_outside and",
    "  lead_misalignment are all detected at high rates.",
    "- 50 permutations per replicate make each null threshold noisy; nominal size with 50",
    "  permutations is about 0.067 by simulation, not 0.05.",
    "- No multiplicity correction is applied across scenarios. All conclusions are exploratory.",
]


def main() -> None:
    data = json.loads((EXP / "controls_results.json").read_text(encoding="utf-8"))
    lines = header(data) + ["", "## Results", ""]
    lines += [
        "Full rule = margin above the block-permutation null 95th percentile AND date",
        "consistency. Wilson 95% intervals on the full-rule rate; margin-only for comparison.",
        "",
    ]
    lines += table(data) + [""] + READING
    (EXP / "synthetic_controls_preliminary.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("wrote", EXP / "synthetic_controls_preliminary.md")


if __name__ == "__main__":
    main()
