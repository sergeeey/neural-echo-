"""Exact binomial table for the NE-EXP-004 candidate-B inflation rule (60 zero-effect replicates).

Rule (fixed in controls.md, C3-B): K = number of rejections of the declared test at alpha 0.05 over
60 independent zero-effect replicates.
  K >= 8  -> INFLATION FLAG
  K <= 7  -> NO GROSS INFLATION DETECTED  (not a demonstration of calibration)

The table gives P(flag) and P(no flag) for several true rejection rates p. Exact binomial, no
approximation. Output is written to binomial_flag_table.txt in the contract folder.
"""

from __future__ import annotations

from math import comb
from pathlib import Path

N = 60
THRESHOLD = 8
TRUE_RATES = (0.031, 0.05, 0.08, 0.10, 0.15, 0.20)
OUT = Path(
    "experiments/20261027-ne-exp-004-wheel-added-information-contract/binomial_flag_table.txt"
)


def p_at_least(k: int, n: int, p: float) -> float:
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


def main() -> None:
    lines = [
        f"Exact binomial, n = {N} independent zero-effect replicates, flag if K >= {THRESHOLD}",
        "",
        "true rate p | P(INFLATION FLAG) | P(NO GROSS INFLATION DETECTED) | E[K]",
        "-----------|------------------|-------------------------------|------",
    ]
    for p in TRUE_RATES:
        flag = p_at_least(THRESHOLD, N, p)
        lines.append(f"{p:10.3f} | {flag:16.4f} | {1 - flag:29.4f} | {N * p:5.2f}")
    lines += [
        "",
        f"Flag threshold as a rate: {THRESHOLD}/{N} = {THRESHOLD / N:.3f}.",
        "Reading: a rule of true size 0.05 is flagged with probability about "
        f"{p_at_least(THRESHOLD, N, 0.05):.4f}; a rule of true size 0.10 is flagged with "
        f"probability {p_at_least(THRESHOLD, N, 0.10):.4f} and passes 'no gross inflation' with "
        f"probability {1 - p_at_least(THRESHOLD, N, 0.10):.4f}.",
        "A 'NO GROSS INFLATION DETECTED' result therefore does not establish calibration: an "
        "inflated rule of true size 0.10 passes it more often than not.",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("saved", OUT)


if __name__ == "__main__":
    main()
