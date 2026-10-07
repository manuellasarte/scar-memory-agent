from datetime import datetime, timezone

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class CapabilityRegistry:
    def __init__(self, conn):
        self.conn = conn

    def register_capability(self, experiment_id, name, origin_scar_id, description=None):
        cur = self.conn.execute(
            """INSERT INTO capabilities
               (experiment_id, name, origin_scar_id, created_at, state,
                utility_score, usage_count, success_count, failure_count, description)
               VALUES (?, ?, ?, ?, 'NACIENTE', 0.0, 0, 0, 0, ?)""",
            (experiment_id, name, origin_scar_id, _now(), description)
        )
        cap_id = cur.lastrowid
        self.conn.execute(
            """INSERT INTO capability_state_history
               (capability_id, previous_state, new_state, changed_at, reason)
               VALUES (?, NULL, 'NACIENTE', ?, ?)""",
            (cap_id, _now(), "initial registration")
        )
        self.conn.commit()
        return cap_id

    def record_usage(self, capability_id, success, error_avoided=None, notes=None):
        self.conn.execute(
            """INSERT INTO capability_usages
               (capability_id, used_at, success, error_avoided, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (capability_id, _now(), 1 if success else 0, error_avoided, notes)
        )
        self.conn.execute(
            """UPDATE capabilities SET
                 usage_count   = usage_count + 1,
                 success_count = success_count + ?,
                 failure_count = failure_count + ?
               WHERE id = ?""",
            (1 if success else 0, 0 if success else 1, capability_id)
        )
        self._recompute_utility(capability_id)
        self.conn.commit()

    def _recompute_utility(self, capability_id):
        row = self.conn.execute(
            "SELECT state, usage_count, success_count FROM capabilities WHERE id = ?",
            (capability_id,)
        ).fetchone()
        if not row:
            return

        score = (row["success_count"] / row["usage_count"]) if row["usage_count"] > 0 else 0.0
        self.conn.execute(
            "UPDATE capabilities SET utility_score = ? WHERE id = ?",
            (round(score, 4), capability_id)
        )

        new_state = row["state"]
        if row["usage_count"] >= 20 and score >= 0.8:
            new_state = "CONSOLIDADA"
        elif row["usage_count"] >= 5 and score >= 0.5:
            new_state = "ACTIVA"

        if new_state != row["state"]:
            self.conn.execute(
                "UPDATE capabilities SET state = ? WHERE id = ?",
                (new_state, capability_id)
            )
            self.conn.execute(
                """INSERT INTO capability_state_history
                   (capability_id, previous_state, new_state, changed_at, reason)
                   VALUES (?, ?, ?, ?, ?)""",
                (capability_id, row["state"], new_state, _now(),
                 "automatic utility-based transition")
            )

    def get_capability(self, capability_id):
        row = self.conn.execute(
            "SELECT * FROM capabilities WHERE id = ?",
            (capability_id,)
        ).fetchone()
        return dict(row) if row else None
