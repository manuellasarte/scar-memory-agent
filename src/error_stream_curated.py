"""
Curated error stream generator.
Generador de flujo de errores curado.

Expands a curated config (error_type, severity, impact, count)
into a deterministic list of events.

Expande una config curada (error_type, severity, impact, count)
en una lista determinista de eventos.
"""

import json
import random
from pathlib import Path


def load_config(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_curated_stream(config):
    rng = random.Random(config["seed"])
    events = []
    for spec in config["curated_stream"]:
        for _ in range(spec["count"]):
            # Jitter tiny, keep deterministic per seed
            sev_jitter = rng.uniform(-0.01, 0.01)
            imp_jitter = rng.uniform(-0.01, 0.01)
            events.append({
                "error_type": spec["error_type"],
                "severity": round(max(0.0, min(1.0, spec["severity"] + sev_jitter)), 4),
                "impact":   round(max(0.0, min(1.0, spec["impact"]   + imp_jitter)), 4),
            })

    rng.shuffle(events)
    for i, e in enumerate(events):
        e["index"] = i
    return events


def save_stream(stream, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(stream, f, indent=2)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    cfg_path = root / "experiments" / "exp_002_rare_severe" / "config.json"
    out_path = root / "experiments" / "exp_002_rare_severe" / "stream.json"

    cfg = load_config(cfg_path)
    stream = generate_curated_stream(cfg)
    save_stream(stream, out_path)

    from collections import Counter
    print(f"[stream] generated {len(stream)} events → {out_path}")
    print("[stream] distribution:", Counter(e["error_type"] for e in stream))
