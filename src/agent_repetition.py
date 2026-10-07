"""
Agent B — Repetition Rule (baseline)
Agente B — Regla de Repetición (línea base)

Forms a scar when the same error type occurs at least N times,
ignoring severity and impact.

Forma una cicatriz cuando el mismo tipo de error ocurre al menos N veces,
ignorando severidad e impacto.
"""

import random
from collections import Counter
from datetime import datetime, timezone

from .wound_manager import WoundManager
from .capability_registry import CapabilityRegistry
from .agent_adaptive_pressure import true_value


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RepetitionAgent:
    name = "repetition_rule"

    def __init__(self, conn, min_repetitions=3, usage_trials=30, usage_seed=999):
        self.conn = conn
        self.wm = WoundManager(conn)
        self.cr = CapabilityRegistry(conn)
        self.min_repetitions = min_repetitions
        self.usage_trials = usage_trials
        self.usage_seed = usage_seed
        self._stream_length = None

    def run(self, stream):
        exp_id = self._create_experiment()
        self._stream_length = len(stream)

        for e in stream:
            self.wm.register_wound(exp_id, e["error_type"], e["severity"], e["impact"])

        counts = Counter(e["error_type"] for e in stream)
        formed = []
        for etype, count in sorted(counts.items()):
            if count < self.min_repetitions:
                continue
            scar_id = self._create_scar(exp_id, etype, count)
            cap_id = self.cr.register_capability(
                exp_id,
                f"capability_for_{etype.lower()}",
                scar_id,
                f"Capability from {etype} scar (repetition rule)",
            )
            formed.append((scar_id, cap_id, etype))

        self._simulate_usage(formed)
        return exp_id, formed

    def _simulate_usage(self, formed):
        rng = random.Random(self.usage_seed)
        for _, cap_id, etype in sorted(formed, key=lambda x: x[2]):
            p = true_value(etype)
            for _ in range(self.usage_trials):
                self.cr.record_usage(cap_id, rng.random() < p)

    def _create_scar(self, exp_id, error_type, count):
        scar_name = f"SCAR_{error_type}"
        existing = self.conn.execute(
            "SELECT id FROM scars WHERE experiment_id = ? AND name = ?",
            (exp_id, scar_name),
        ).fetchone()
        if existing:
            return existing["id"]

        # Normalize count into the same [0,1] scale used by the pressure agent.
        # Normalizamos el conteo a la misma escala [0,1] usada por el agente de presión.
        stream_length = self._stream_length if self._stream_length else 1
        normalized_pressure = round(count / stream_length, 4)

        cur = self.conn.execute(
            """INSERT INTO scars
               (experiment_id, name, created_at, scar_pressure, threshold,
                formula_version, status, description)
               VALUES (?, ?, ?, ?, ?, ?, 'ACTIVE', ?)""",
            (exp_id, scar_name, _now(), normalized_pressure, float(self.min_repetitions),
             "v1_repetition",
             f"Scar formed by repetition (count={count}, stream_length={stream_length})"),
        )
        scar_id = cur.lastrowid

        rows = self.conn.execute(
            "SELECT id FROM wounds WHERE experiment_id = ? AND error_type = ?",
            (exp_id, error_type),
        ).fetchall()
        for r in rows:
            self.conn.execute(
                """INSERT OR IGNORE INTO scar_wounds
                   (scar_id, wound_id, contribution) VALUES (?, ?, ?)""",
                (scar_id, r["id"], round(1.0 / len(rows), 4)),
            )
        self.conn.commit()
        return scar_id

    def _create_experiment(self):
        cur = self.conn.execute(
            "INSERT INTO experiments (name, started_at, notes) VALUES (?, ?, ?)",
            (f"exp_001_{self.name}", _now(), "Agent B - repetition rule"),
        )
        self.conn.commit()
        return cur.lastrowid
