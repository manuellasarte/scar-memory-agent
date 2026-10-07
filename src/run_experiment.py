"""
Experiment 001 runner — Pressure vs Repetition
Ejecutor del Experimento 001 — Presión vs Repetición

Runs both agents on the same stream, computes metrics,
and writes raw + summary results.

Ejecuta ambos agentes sobre el mismo flujo, calcula métricas
y escribe resultados crudos + resumen.
"""

import csv
import json
from pathlib import Path

from .db import init_db
from .agent_adaptive_pressure import AdaptivePressureAgent
from .agent_repetition import RepetitionAgent


ROOT = Path(__file__).resolve().parent.parent
EXP_DIR = ROOT / "experiments" / "exp_001_pressure_vs_repetition"
RESULTS_DIR = ROOT / "results" / "exp_001"


def compute_metrics(conn, experiment_id, stream, agent_label):
    scars = conn.execute(
        "SELECT name FROM scars WHERE experiment_id = ?", (experiment_id,)
    ).fetchall()
    caps = conn.execute(
        """SELECT state, utility_score FROM capabilities
           WHERE experiment_id = ?""",
        (experiment_id,),
    ).fetchall()

    scar_types = {s["name"].replace("SCAR_", "") for s in scars}
    stream_types = {e["error_type"] for e in stream}

    scar_count = len(scars)
    cap_count = len(caps)

    utilities = [c["utility_score"] for c in caps]
    avg_utility = round(sum(utilities) / len(utilities), 4) if utilities else 0.0

    surviving = sum(1 for c in caps if c["state"] in ("ACTIVA", "CONSOLIDADA"))
    survival_rate = round(surviving / cap_count, 4) if cap_count else 0.0

    false_scars = {t for t in scar_types if t == "TRIVIAL"}
    false_scar_rate = round(len(false_scars) / scar_count, 4) if scar_count else 0.0

    missed = {t for t in stream_types if t == "SEVERE" and t not in scar_types}
    missed_scar_rate = 1.0 if missed else 0.0

    return {
        "agent": agent_label,
        "scar_count": scar_count,
        "capability_count": cap_count,
        "avg_utility": avg_utility,
        "survival_rate": survival_rate,
        "false_scar_rate": false_scar_rate,
        "missed_scar_rate": missed_scar_rate,
    }


def main():
    db_path = ROOT / "data" / "scar_memory.db"
    if db_path.exists():
        db_path.unlink()
    conn = init_db()

    with (EXP_DIR / "stream.json").open("r", encoding="utf-8") as f:
        stream = json.load(f)

    agent_a = AdaptivePressureAgent(conn, threshold=0.55)
    exp_a, formed_a = agent_a.run(stream)

    agent_b = RepetitionAgent(conn, min_repetitions=3)
    exp_b, formed_b = agent_b.run(stream)

    m_a = compute_metrics(conn, exp_a, stream, "adaptive_pressure")
    m_b = compute_metrics(conn, exp_b, stream, "repetition_rule")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with (RESULTS_DIR / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(
            {"experiment_id": "exp_001", "agent_a": m_a, "agent_b": m_b},
            f, indent=2,
        )

    with (RESULTS_DIR / "raw.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["agent", "scar_count", "capability_count", "avg_utility",
                         "survival_rate", "false_scar_rate", "missed_scar_rate"])
        for m in (m_a, m_b):
            writer.writerow([m["agent"], m["scar_count"], m["capability_count"],
                             m["avg_utility"], m["survival_rate"],
                             m["false_scar_rate"], m["missed_scar_rate"]])

    print("=== Agent A: adaptive_pressure ===")
    for k, v in m_a.items():
        print(f"  {k}: {v}")
    print("=== Agent B: repetition_rule ===")
    for k, v in m_b.items():
        print(f"  {k}: {v}")
    print(f"\nsummary → {RESULTS_DIR / 'summary.json'}")
    print(f"raw     → {RESULTS_DIR / 'raw.csv'}")


if __name__ == "__main__":
    main()
