# Experiment 001 — Results

# English

## Description

Comparison between two scar formation mechanisms exposed to the
same synthetic error stream of 500 events:

- A: Adaptive Pressure (this project)
- B: Repetition Rule (3 identical failures → scar)

---

## Files

- `summary.json` — per-agent metrics
- `deltas.json` — difference A − B and relative improvements
- `raw.csv` — flat table of both agents
- `table.tex` — LaTeX table ready to include in the paper

---

## Key Findings

- Adaptive pressure forms fewer scars but with higher average utility.
- Repetition forms a false-positive scar from TRIVIAL events.
- Adaptive pressure achieved a higher capability survival rate.

---

## Interpretation

The mechanism is not "counting errors" but "measuring adaptive pressure".
This distinction is what allows the system to detect rare but severe
failures while ignoring repeated but trivial ones.

---

# Español

## Descripción

Comparación entre dos mecanismos de formación de cicatrices expuestos
al mismo flujo sintético de 500 eventos:

- A: Presión Adaptativa (este proyecto)
- B: Regla de Repetición (3 fallos idénticos → cicatriz)

---

## Ficheros

- `summary.json` — métricas por agente
- `deltas.json` — diferencia A − B y mejoras relativas
- `raw.csv` — tabla plana de ambos agentes
- `table.tex` — tabla LaTeX lista para incluir en el paper

---

## Hallazgos Clave

- La presión adaptativa forma menos cicatrices pero de mayor utilidad promedio.
- La repetición forma una cicatriz falsa a partir de eventos TRIVIAL.
- La presión adaptativa logró mayor tasa de supervivencia de capacidades.

---

## Interpretación

El mecanismo no es "contar errores" sino "medir presión adaptativa".
Esa distinción es lo que permite detectar fallos raros pero graves
mientras se ignoran los repetidos pero triviales.
