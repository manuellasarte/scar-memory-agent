"""
Multi-seed robustness study for Experiment 001.
Estudio de robustez multi-semilla para el Experimento 001.

Runs Experiment 001 across N independent seeds and reports
mean +/- std per metric for both agents.
"""

import csv
import json
import random
from pathlib import Path
from statistics import mean, stdev

from .db import init_db
from .wound_manager import WoundManager
from .scar_formation import ScarFormation
from .capability_registry import CapabilityRegistry
from .agent_adaptive_pressure import true_value


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "results" / "exp_001_multiseed"


def generate_stream(seed, length, dist):
    rng = random.Random(seed)
    types = list(dist.keys())
    weights = [dist[t]["probability"] for t in types]
    stream = []
    for i in range(length):
        etype = rng.choices(types, weights=weights, k=1)[0]
        sev_lo, sev_hi = dist[etype]["severity_range"]
        imp_lo, imp_hi = dist[etype]["impact_range"]
        stream.append({
            "index": i,
            "error_type": etype,
            "severity": round(rng.uniform(sev_lo, sev_hi), 4),
            "impact": round(rng.uniform(imp_lo, imp_hi), 4),
        })
    return stream


def run_single_trial(conn, stream, seed):
    """Run both agents on the same stream under a fresh experiment."""
    from datetime import datetime, timezone
    def now():
        return datetime.now(timezone.utc).isoformat()

    # Agent A
    cur = conn.execute(
        "INSERT INTO experiments (name, started_at, notes) VALUES (?, ?, ?)",
        (f"multiseed_A_seed{seed}", now(), f"seed={seed}")
    )
    exp_a = cur.lastrowid

    wm = WoundManager(conn)
    for e in stream:
        wm.register_wound(exp_a, e["error_type"], e["severity"], e["impact"])

    sf = ScarFormation(conn, threshold=0.55)
    cr = CapabilityRegistry(conn)
    formed_a = []
    for etype in sorted({e["error_type"] for e in stream}):
        r = sf.evaluate_error_type(exp_a, etype)
        if r.get("formed"):
            cid = cr.register_capability(
                exp_a, f"cap_a_{etype.lower()}", r["scar_id"], "A"
            )
            formed_a.append((cid, etype))

    rng = random.Random(seed + 1000)
    for cid, etype in sorted(formed_a, key=lambda x: x[1]):
        p = true_value(etype)
        for _ in range(30):
            cr.record_usage(cid, rng.random() < p)

    # Agent B
    cur = conn.execute(
        "INSERT INTO experiments (name, started_at, notes) VALUES (?, ?, ?)",
        (f"multiseed_B_seed{seed}", now(), f"seed={seed}")
    )
    exp_b = cur.lastrowid

    for e in stream:
        wm.register_wound(exp_b, e["error_type"], e["severity"], e["impact"])

    from collections import Counter
    counts = Counter(e["error_type"] for e in stream)
    formed_b = []
    for etype, c in sorted(counts.items()):
        if c < 3:
            continue
        cur = conn.execute(
            """INSERT INTO scars
               (experiment_id, name, created_at, scar_pressure, threshold,
                formula_version, status, description)
               VALUES (?, ?, ?, ?, ?, ?, 'ACTIVE', ?)""",
            (exp_b, f"SCAR_{etype}", now(), round(c / len(stream), 4),
             3.0, "v1_repetition", f"repetition count={c}")
        )
        sid = cur.lastrowid
        cid = cr.register_capability(exp_b, f"cap_b_{etype.lower()}", sid, "B")
        formed_b.append((cid, etype))

    rng = random.Random(seed + 1000)
    for cid, etype in sorted(formed_b, key=lambda x: x[1]):
        p = true_value(etype)
        for _ in range(30):
            cr.record_usage(cid, rng.random() < p)

    conn.commit()
    return exp_a, exp_b


def metrics_for(conn, exp_id, stream, severe_types):
    scars = conn.execute(
        "SELECT name FROM scars WHERE experiment_id = ?", (exp_id,)
    ).fetchall()
    caps = conn.execute(
        "SELECT state, utility_score FROM capabilities WHERE experiment_id = ?",
        (exp_id,)
    ).fetchall()

    scar_types = {s["name"].replace("SCAR_", "") for s in scars}
    scar_count = len(scars)
    cap_count = len(caps)
    utilities = [c["utility_score"] for c in caps]
    avg_util = sum(utilities) / len(utilities) if utilities else 0.0
    surviving = sum(1 for c in caps if c["state"] in ("ACTIVA", "CONSOLIDADA"))
    surv = surviving / cap_count if cap_count else 0.0
    false_scars = {t for t in scar_types if t.startswith("TRIVIAL")}
    false_rate = len(false_scars) / scar_count if scar_count else 0.0
    missed = severe_types - scar_types
    missed_rate = len(missed) / len(severe_types) if severe_types else 0.0

    return {
        "scar_count": scar_count,
        "capability_count": cap_count,
        "avg_utility": round(avg_util, 4),
        "survival_rate": round(surv, 4),
        "false_scar_rate": round(false_rate, 4),
        "missed_scar_rate": round(missed_rate, 4),
    }


def main(n_seeds=10):
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    dist = {
        "TRIVIAL":  {"probability": 0.5, "severity_range": [0.05, 0.20], "impact_range": [0.05, 0.20]},
        "MODERATE": {"probability": 0.3, "severity_range": [0.40, 0.60], "impact_range": [0.40, 0.60]},
        "SEVERE":   {"probability": 0.2, "severity_range": [0.85, 1.00], "impact_range": [0.85, 1.00]},
    }
    severe_types = {"SEVERE"}

    all_a = []
    all_b = []

    for seed in range(n_seeds):
        conn = init_db()

        # Limpiar la base entre trials
        for table in ("capability_state_history", "capability_usages",
                      "capabilities", "scar_wounds", "scars",
                      "wounds", "experiments"):
            conn.execute(f"DELETE FROM {table}")
        conn.commit()

        stream = generate_stream(seed, 500, dist)
        exp_a, exp_b = run_single_trial(conn, stream, seed)
        ma = metrics_for(conn, exp_a, stream, severe_types)
        mb = metrics_for(conn, exp_b, stream, severe_types)
        ma["seed"] = seed
        mb["seed"] = seed
        all_a.append(ma)
        all_b.append(mb)
        conn.close()

    metrics = ["scar_count", "capability_count", "avg_utility",
               "survival_rate", "false_scar_rate", "missed_scar_rate"]

    # Direction per metric: +1 means higher is better, -1 means lower is better
    direction = {
        "scar_count": 0,          # neutral (context-dependent)
        "capability_count": 0,    # neutral
        "avg_utility": +1,
        "survival_rate": +1,
        "false_scar_rate": -1,
        "missed_scar_rate": -1,
    }

    summary = {"n_seeds": n_seeds, "metrics": {}}
    for m in metrics:
        va = [x[m] for x in all_a]
        vb = [x[m] for x in all_b]
        d = direction.get(m, 0)
        if d == 0:
            wins = None
        elif d > 0:
            wins = sum(1 for x, y in zip(va, vb) if x > y)
        else:
            wins = sum(1 for x, y in zip(va, vb) if x < y)
        summary["metrics"][m] = {
            "A_mean": round(mean(va), 4),
            "A_std":  round(stdev(va), 4) if len(va) > 1 else 0.0,
            "B_mean": round(mean(vb), 4),
            "B_std":  round(stdev(vb), 4) if len(vb) > 1 else 0.0,
            "delta_mean": round(mean(va) - mean(vb), 4),
            "direction": d,
            "A_wins": wins,
            "n": n_seeds,
        }

    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    with (OUT_DIR / "raw.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["seed", "agent"] + metrics)
        for a, b in zip(all_a, all_b):
            w.writerow([a["seed"], "A"] + [a[m] for m in metrics])
            w.writerow([b["seed"], "B"] + [b[m] for m in metrics])

    print(f"[multiseed] {n_seeds} seeds completed")
    for m in metrics:
        s = summary["metrics"][m]
        wins_str = f"{s['A_wins']}/{s['n']}" if s['A_wins'] is not None else "n/a"
        print(f"  {m:20s}  A={s['A_mean']:.4f}+/-{s['A_std']:.4f}  "
              f"B={s['B_mean']:.4f}+/-{s['B_std']:.4f}  "
              f"delta={s['delta_mean']:+.4f}  A_wins={wins_str}")

    print(f"summary -> {OUT_DIR / 'summary.json'}")
    print(f"raw     -> {OUT_DIR / 'raw.csv'}")


if __name__ == "__main__":
    main()
