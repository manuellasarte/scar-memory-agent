"""
Agent A — Adaptive Pressure
Agente A — Presión Adaptativa

Consumes the shared error stream and forms scars only when
adaptive pressure exceeds a threshold.

Consume el flujo de errores compartido y forma cicatrices solo
cuando la presión adaptativa supera un umbral.
"""

import random
from datetime import datetime, timezone

from .wound_manager import WoundManager
from .scar_formation import ScarFormation
from .capability_registry import CapabilityRegistry


def true_value(error_type: str) -> float:
    """
    Declared utility model for the paper.
    Modelo de utilidad declarado para el paper.

    TRIVIAL*  → 0.2
    MODERATE* → 0.6
    SEVERE*   → 0.9

    This is a modeling assumption, not an empirical measurement.
    Es una asunción de modelado, no una medición empírica.
    """
    if error_type.startswith("TRIVIAL"):
        return 0.2
    if error_type.startswith("MODERATE"):
        return 0.6
    if error_type.startswith("SEVERE"):
        return 0.9
    return 0.5


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class AdaptivePressureAgent:
    name = "adaptive_pressure"

    def __init__(self, conn, threshold=0.55, usage_trials=30, usage_seed=999):
        self.conn = conn
        self.wm = WoundManager(conn)
        self.sf = ScarFormation(conn, threshold=threshold)
        self.cr = CapabilityRegistry(conn)
        self.usage_trials = usage_trials
        self.usage_seed = usage_seed

    def run(self, stream):
        exp_id = self._create_experiment()
        for e in stream:
            self.wm.register_wound(exp_id, e["error_type"], e["severity"], e["impact"])

        formed = []
        for etype in sorted({e["error_type"] for e in stream}):
            res = self.sf.evaluate_error_type(exp_id, etype)
            if res.get("formed"):
                cap_id = self.cr.register_capability(
                    exp_id,
                    f"capability_for_{etype.lower()}",
                    res["scar_id"],
                    f"Capability from {etype} scar (adaptive pressure)",
                )
                formed.append((res["scar_id"], cap_id, etype))

        self._simulate_usage(formed)
        return exp_id, formed

    def _simulate_usage(self, formed):
        rng = random.Random(self.usage_seed)
        for _, cap_id, etype in sorted(formed, key=lambda x: x[2]):
            p = true_value(etype)
            for _ in range(self.usage_trials):
                self.cr.record_usage(cap_id, rng.random() < p)

    def _create_experiment(self):
        cur = self.conn.execute(
            "INSERT INTO experiments (name, started_at, notes) VALUES (?, ?, ?)",
            (f"exp_001_{self.name}", _now(), "Agent A - adaptive pressure"),
        )
        self.conn.commit()
        return cur.lastrowid
