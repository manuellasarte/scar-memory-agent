from datetime import datetime, timezone

from .db import init_db
from .wound_manager import WoundManager
from .scar_formation import ScarFormation
from .capability_registry import CapabilityRegistry


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main():
    conn = init_db()
    wm = WoundManager(conn)
    sf = ScarFormation(conn, threshold=0.55)
    cr = CapabilityRegistry(conn)

    # 1. Experimento
    cur = conn.execute(
        "INSERT INTO experiments (name, started_at, notes) VALUES (?, ?, ?)",
        ("first_pipeline_run", _now(), "Fase 1.5 - primera integración real")
    )
    exp_id = cur.lastrowid
    conn.commit()
    print(f"[experiment] id={exp_id}")

    # 2. Heridas
    wounds = [
        ("DEPENDENCY_RESOLUTION_FAILURE", 0.7, 0.8),
        ("DEPENDENCY_RESOLUTION_FAILURE", 0.6, 0.7),
        ("DEPENDENCY_RESOLUTION_FAILURE", 0.8, 0.9),
        ("DEPENDENCY_RESOLUTION_FAILURE", 0.75, 0.85),
        ("MINOR_TIMEOUT", 0.1, 0.1),
    ]
    for et, sev, imp in wounds:
        wid = wm.register_wound(exp_id, et, sev, imp)
        print(f"[wound] id={wid} type={et} severity={sev} impact={imp}")

    # 3. Formación de cicatriz
    result = sf.evaluate_error_type(exp_id, "DEPENDENCY_RESOLUTION_FAILURE")
    print(f"[scar] {result}")

    if not result.get("formed"):
        print("[scar] No se formó cicatriz. Fin del pipeline.")
        conn.close()
        return

    # 4. Capacidad emergente
    cap_id = cr.register_capability(
        exp_id,
        "dependency_validation",
        result["scar_id"],
        "Valida dependencias antes de resolverse"
    )
    print(f"[capability] id={cap_id} origin_scar={result['scar_id']}")

    # 5. Simulación de usos
    for i in range(25):
        success = i not in (3, 7, 12, 20)
        cr.record_usage(cap_id, success)

    # 6. Estado final
    final = cr.get_capability(cap_id)
    print("[final capability]")
    for k, v in final.items():
        print(f"   {k}: {v}")

    conn.close()


if __name__ == "__main__":
    main()
