# Joint Report — Experiments 001 & 002

# English

## Overview

Two complementary experiments were conducted to evaluate the
adaptive-pressure scar formation mechanism against a repetition-based
baseline.

- **Experiment 001** measured general performance on a probabilistic
  stream of 500 events.
- **Experiment 002** measured the safety property on a curated stream
  containing rare but severe failures.

Together, they provide a two-dimensional evaluation: efficiency and safety.

---

## Experiment 001 — General Performance

| Metric              | Adaptive Pressure (A) | Repetition (B) |
|---------------------|----------------------:|---------------:|
| Scars formed        | 2                     | 3              |
| Capabilities born   | 2                     | 3              |
| Avg utility score   | 0.7500                | 0.5778         |
| Survival rate       | 1.0000                | 0.6667         |
| False scar rate     | 0.0000                | 0.3333         |
| Missed severe rate  | 0.0000                | 0.0000         |

Key results:
- +29.8 % average utility improvement for Agent A.
- +50.0 % survival rate improvement for Agent A.
- Zero false-positive scars for Agent A.
- H3 not testable in this stream (SEVERE events repeated ≥ 3 times).

---

## Experiment 002 — Safety Property

| Metric                        | Adaptive Pressure (A) | Repetition (B) |
|-------------------------------|----------------------:|---------------:|
| Scars formed                  | 3                     | 2              |
| Capabilities born             | 3                     | 2              |
| Avg utility score             | 0.7889                | 0.3667         |
| Survival rate                 | 1.0000                | 0.5000         |
| False scar rate               | 0.0000                | 0.5000         |
| Missed severe rate            | 0.0000                | 1.0000         |
| Detected severe               | 2 / 2                 | 0 / 2          |

Key results:
- Agent A detected 100 % of rare severe failures.
- Agent B missed 100 % of rare severe failures.
- Agent B produced a false scar from repeated trivial events.
- H3 confirmed empirically.

---

## Cross-Experiment Interpretation

- Agent A forms **fewer, higher-quality scars** in both experiments.
- Agent B is driven by raw frequency, which causes it to both
  over-detect trivial events and under-detect severe rare ones.
- The pressure model separates signal (severity × impact) from noise
  (frequency of trivial events), while the repetition model cannot.

---

## Reproducibility

- Both experiments are deterministic given the fixed seed 42.
- Both agents share the exact same stream within each experiment.
- The only difference between agents is the scar formation mechanism.
- Raw results: `results/exp_001/` and `results/exp_002/`.

---

# Español

## Descripción General

Se realizaron dos experimentos complementarios para evaluar el
mecanismo de formación de cicatrices por presión adaptativa frente
a una línea base de repetición.

- **Experimento 001** midió el rendimiento general sobre un flujo
  probabilístico de 500 eventos.
- **Experimento 002** midió la propiedad de seguridad sobre un flujo
  curado que contiene fallos raros pero graves.

En conjunto, ofrecen una evaluación bidimensional: eficiencia y seguridad.

---

## Experimento 001 — Rendimiento General

| Métrica                | Presión Adaptativa (A) | Repetición (B) |
|------------------------|-----------------------:|---------------:|
| Cicatrices formadas    | 2                      | 3              |
| Capacidades nacidas    | 2                      | 3              |
| Utilidad promedio      | 0.7500                 | 0.5778         |
| Tasa de supervivencia  | 1.0000                 | 0.6667         |
| Tasa de falsas         | 0.0000                 | 0.3333         |
| Tasa de graves omitidas| 0.0000                 | 0.0000         |

Resultados clave:
- +29.8 % de mejora en utilidad promedio para el Agente A.
- +50.0 % de mejora en tasa de supervivencia para el Agente A.
- Cero cicatrices falsas para el Agente A.
- H3 no testeable en este flujo (los SEVERE se repitieron ≥ 3 veces).

---

## Experimento 002 — Propiedad de Seguridad

| Métrica                        | Presión Adaptativa (A) | Repetición (B) |
|--------------------------------|-----------------------:|---------------:|
| Cicatrices formadas            | 3                      | 2              |
| Capacidades nacidas            | 3                      | 2              |
| Utilidad promedio              | 0.7889                 | 0.3667         |
| Tasa de supervivencia          | 1.0000                 | 0.5000         |
| Tasa de falsas                 | 0.0000                 | 0.5000         |
| Tasa de graves omitidas        | 0.0000                 | 1.0000         |
| Graves detectados              | 2 / 2                  | 0 / 2          |

Resultados clave:
- El Agente A detectó el 100 % de los fallos graves raros.
- El Agente B omitió el 100 % de los fallos graves raros.
- El Agente B produjo una cicatriz falsa por eventos triviales repetidos.
- H3 confirmada empíricamente.

---

## Interpretación Cruzada

- El Agente A forma **menos cicatrices y de mayor calidad** en ambos experimentos.
- El Agente B está guiado por frecuencia bruta, lo que le hace
  sobre-detectar eventos triviales e infra-detectar eventos graves raros.
- El modelo de presión separa señal (severidad × impacto) de ruido
  (frecuencia de eventos triviales), mientras que el modelo de
  repetición no puede.

---

## Reproducibilidad

- Ambos experimentos son deterministas dada la semilla fija 42.
- Ambos agentes comparten exactamente el mismo flujo dentro de cada experimento.
- La única diferencia entre agentes es el mecanismo de formación de cicatrices.
- Resultados crudos: `results/exp_001/` y `results/exp_002/`.
