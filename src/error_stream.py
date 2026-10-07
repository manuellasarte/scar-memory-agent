import json
import random
from pathlib import Path


def load_config(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_stream(config: dict) -> list[dict]:
    """
    Genera un flujo de errores sintético reproducible.
    El mismo stream se usará para los agentes A y B.
    """
    rng = random.Random(config["seed"])
    length = config["stream_length"]
    dist = config["error_distribution"]

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
            "impact":   round(rng.uniform(imp_lo, imp_hi), 4),
        })
    return stream


def save_stream(stream: list[dict], path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(stream, f, indent=2)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    cfg_path = root / "experiments" / "exp_001_pressure_vs_repetition" / "config.json"
    out_path = root / "experiments" / "exp_001_pressure_vs_repetition" / "stream.json"

    cfg = load_config(cfg_path)
    stream = generate_stream(cfg)
    save_stream(stream, out_path)

    print(f"[stream] generated {len(stream)} events → {out_path}")
    from collections import Counter
    print("[stream] distribution:", Counter(e["error_type"] for e in stream))
