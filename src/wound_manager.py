from datetime import datetime, timezone

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class WoundManager:
    def __init__(self, conn):
        self.conn = conn

    def register_wound(self, experiment_id, error_type, severity, impact,
                       description=None, context_json=None):
        cur = self.conn.execute(
            """INSERT INTO wounds
               (experiment_id, created_at, error_type, severity, impact, description, context_json)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (experiment_id, _now(), error_type, severity, impact, description, context_json)
        )
        self.conn.commit()
        return cur.lastrowid

    def list_wounds(self, experiment_id=None):
        if experiment_id is not None:
            cur = self.conn.execute(
                "SELECT * FROM wounds WHERE experiment_id = ? ORDER BY id",
                (experiment_id,)
            )
        else:
            cur = self.conn.execute("SELECT * FROM wounds ORDER BY id")
        return [dict(r) for r in cur.fetchall()]
