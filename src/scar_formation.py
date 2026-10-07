from datetime import datetime, timezone

FORMULA_VERSION = "v1"
DEFAULT_THRESHOLD = 0.55


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def compute_scar_pressure(frequency, severity, impact) -> float:
    """
    Scar Pressure v1
    frequency: número de heridas del mismo tipo (se normaliza contra 10)
    severity:  promedio de severidad (0..1)
    impact:    promedio de impacto   (0..1)
    """
    freq_norm = min(frequency / 10.0, 1.0)
    return round((freq_norm * 0.4) + (severity * 0.3) + (impact * 0.3), 4)


class ScarFormation:
    def __init__(self, conn, threshold=DEFAULT_THRESHOLD):
        self.conn = conn
        self.threshold = threshold

    def evaluate_error_type(self, experiment_id, error_type):
        rows = self.conn.execute(
            """SELECT id, severity, impact FROM wounds
               WHERE experiment_id = ? AND error_type = ?""",
            (experiment_id, error_type)
        ).fetchall()

        if not rows:
            return {"formed": False, "reason": "no_wounds"}

        frequency = len(rows)
        severity = sum(r["severity"] for r in rows) / frequency
        impact = sum(r["impact"] for r in rows) / frequency
        pressure = compute_scar_pressure(frequency, severity, impact)

        if pressure < self.threshold:
            return {"formed": False, "pressure": pressure, "threshold": self.threshold}

        scar_name = f"SCAR_{error_type}"
        existing = self.conn.execute(
            "SELECT id FROM scars WHERE experiment_id = ? AND name = ?",
            (experiment_id, scar_name)
        ).fetchone()

        if existing:
            scar_id = existing["id"]
            self.conn.execute(
                "UPDATE scars SET scar_pressure = ?, status = 'ACTIVE' WHERE id = ?",
                (pressure, scar_id)
            )
        else:
            cur = self.conn.execute(
                """INSERT INTO scars
                   (experiment_id, name, created_at, scar_pressure, threshold,
                    formula_version, status, description)
                   VALUES (?, ?, ?, ?, ?, ?, 'ACTIVE', ?)""",
                (experiment_id, scar_name, _now(), pressure, self.threshold,
                 FORMULA_VERSION, f"Scar formed from {error_type}")
            )
            scar_id = cur.lastrowid

        for r in rows:
            self.conn.execute(
                """INSERT OR IGNORE INTO scar_wounds (scar_id, wound_id, contribution)
                   VALUES (?, ?, ?)""",
                (scar_id, r["id"], round(1.0 / frequency, 4))
            )

        self.conn.commit()
        return {
            "formed": True,
            "scar_id": scar_id,
            "scar_name": scar_name,
            "pressure": pressure,
            "threshold": self.threshold,
            "wounds_linked": frequency,
        }
