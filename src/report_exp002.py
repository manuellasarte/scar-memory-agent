"""
Experiment 002 report generator.
Generador de informe del Experimento 002.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results" / "exp_002"


def compute_deltas(a: dict, b: dict) -> dict:
    def rel(x, y):
        return round((x - y) / y, 4) if y != 0 else None

    return {
        "scar_count_delta":       a["scar_count"]       - b["scar_count"],
        "capability_count_delta": a["capability_count"] - b["capability_count"],
        "avg_utility_delta":      round(a["avg_utility"] - b["avg_utility"], 4),
        "survival_rate_delta":    round(a["survival_rate"] - b["survival_rate"], 4),
        "false_scar_rate_delta":  round(a["false_scar_rate"] - b["false_scar_rate"], 4),
        "missed_scar_rate_delta": round(a["missed_scar_rate"] - b["missed_scar_rate"], 4),
        "avg_utility_rel_improvement":   rel(a["avg_utility"], b["avg_utility"]),
        "survival_rate_rel_improvement": rel(a["survival_rate"], b["survival_rate"]),
    }


def write_latex_table(a: dict, b: dict, path: Path) -> None:
    rows = [
        ("Scars formed",       a["scar_count"],       b["scar_count"]),
        ("Capabilities born",  a["capability_count"], b["capability_count"]),
        ("Avg utility score",  a["avg_utility"],      b["avg_utility"]),
        ("Survival rate",      a["survival_rate"],    b["survival_rate"]),
        ("False scar rate",    a["false_scar_rate"],  b["false_scar_rate"]),
        ("Missed severe rate", a["missed_scar_rate"], b["missed_scar_rate"]),
    ]

    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\caption{Experiment 002 - Rare Severe Failures. "
                 r"Lower is better for \textit{False scar rate} and \textit{Missed severe rate}.}")
    lines.append(r"\label{tab:exp002}")
    lines.append(r"\begin{tabular}{lcc}")
    lines.append(r"\hline")
    lines.append(r"\textbf{Metric} & \textbf{Adaptive Pressure (A)} & \textbf{Repetition (B)} \\")
    lines.append(r"\hline")
    for label, va, vb in rows:
        lines.append(f"{label} & {va} & {vb} \\\\")
    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    with (RESULTS / "summary.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

    a = data["agent_a"]
    b = data["agent_b"]

    deltas = compute_deltas(a, b)
    (RESULTS / "deltas.json").write_text(
        json.dumps(deltas, indent=2), encoding="utf-8"
    )

    write_latex_table(a, b, RESULTS / "table.tex")

    print("[report] deltas.json written")
    for k, v in deltas.items():
        print(f"   {k}: {v}")
    print("[report] table.tex written")


if __name__ == "__main__":
    main()
