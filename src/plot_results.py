"""
Generate a bar-chart comparison of Agent A vs Agent B for both experiments.
Genera una comparacion de barras del Agente A vs Agente B para ambos experimentos.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
FIG_DIR = ROOT / "paper" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


METRICS = [
    ("avg_utility",      "Avg utility"),
    ("survival_rate",    "Survival rate"),
    ("false_scar_rate",  "False scar rate"),
    ("missed_scar_rate", "Missed severe rate"),
]


def load(exp):
    with (RESULTS / exp / "summary.json").open() as f:
        return json.load(f)


def plot_experiment(ax, data, title):
    a = data["agent_a"]
    b = data["agent_b"]

    labels = [m[1] for m in METRICS]
    vals_a = [a[m[0]] for m in METRICS]
    vals_b = [b[m[0]] for m in METRICS]

    x = np.arange(len(labels))
    w = 0.38

    ax.bar(x - w/2, vals_a, w, label="Adaptive Pressure (A)", color="#2b7a78")
    ax.bar(x + w/2, vals_b, w, label="Repetition (B)",       color="#c94c4c")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    ax.set_title(title)
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    ax.legend(loc="upper right", fontsize=8)

    for i, v in enumerate(vals_a):
        ax.text(i - w/2, v + 0.02, f"{v:.2f}", ha="center", fontsize=7)
    for i, v in enumerate(vals_b):
        ax.text(i + w/2, v + 0.02, f"{v:.2f}", ha="center", fontsize=7)


def main():
    exp1 = load("exp_001")
    exp2 = load("exp_002")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    plot_experiment(axes[0], exp1, "Experiment 001 -- General Performance")
    plot_experiment(axes[1], exp2, "Experiment 002 -- Safety Property")

    fig.suptitle(
        "Adaptive Pressure vs Repetition: comparative results",
        fontsize=12, fontweight="bold"
    )
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    out_png = FIG_DIR / "results_comparison.png"
    out_svg = FIG_DIR / "results_comparison.svg"
    fig.savefig(out_png, dpi=180)
    fig.savefig(out_svg)
    plt.close(fig)

    print("OK ->", out_png)
    print("OK ->", out_svg)


if __name__ == "__main__":
    main()
