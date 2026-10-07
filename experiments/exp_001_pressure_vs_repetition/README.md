# Experiment 001 — Pressure vs Repetition

# English

## Objective

Test whether adaptive-pressure scar formation produces more useful
capabilities than repetition-based scar formation.

---

## Hypotheses

- H1: Pressure-based formation yields higher average capability utility.
- H2: Pressure-based formation produces fewer false-positive scars.
- H3: Pressure-based formation detects severe rare failures that
      repetition-based formation would miss.

---

## Baselines

- A: Adaptive Pressure (this project)
- B: Repetition Rule (3 identical failures → scar)

---

## Metrics

- scar_count
- capability_count
- avg_utility
- survival_rate
- false_scar_rate
- missed_scar_rate

---

## Reproducibility

- Fixed random seed (42)
- Identical error stream shared by both agents
- Configuration stored in config.json
- Raw results in results/exp_001/raw.csv

---

# Español

## Objetivo

Comprobar si la formación de cicatrices por presión adaptativa produce
capacidades más útiles que la formación por repetición.

---

## Hipótesis

- H1: La formación por presión produce mayor utilidad promedio de capacidad.
- H2: La formación por presión produce menos cicatrices falsas.
- H3: La formación por presión detecta fallos graves y raros que la
      formación por repetición pasaría por alto.

---

## Líneas Base

- A: Presión Adaptativa (este proyecto)
- B: Regla de Repetición (3 fallos idénticos → cicatriz)

---

## Métricas

- scar_count
- capability_count
- avg_utility
- survival_rate
- false_scar_rate
- missed_scar_rate

---

## Reproducibilidad

- Semilla fija (42)
- Flujo de errores idéntico compartido por ambos agentes
- Configuración guardada en config.json
- Resultados crudos en results/exp_001/raw.csv
