# Experiment 002 — Rare Severe Failures

# English

## Objective

Verify H3 from Experiment 001: whether adaptive-pressure scar formation
detects rare but severe failures that repetition-based formation ignores.

---

## Design

Instead of a probabilistic distribution, the stream is curated:

| Error type               | Severity | Impact | Count |
|--------------------------|---------:|-------:|------:|
| TRIVIAL_LOG_NOISE        | 0.10     | 0.10   | 25    |
| MODERATE_TIMEOUT         | 0.50     | 0.55   | 6     |
| SEVERE_DATA_CORRUPTION   | 0.95     | 0.99   | 1     |
| SEVERE_AUTH_BYPASS       | 0.90     | 0.95   | 2     |

The SEVERE events occur only 1 and 2 times respectively — below the
threshold of 3 required by the repetition rule.

---

## Hypothesis

- A (Adaptive Pressure) forms scars for SEVERE_DATA_CORRUPTION and
  SEVERE_AUTH_BYPASS because their pressure exceeds 0.55.
- B (Repetition) does not form scars for either, because neither
  reaches 3 repetitions.

---

## Expected Outcome

- Missed severe rate: A = 0.0, B = 1.0.
- This confirms that pressure-based formation provides a safety
  property that repetition-based formation cannot.

---

## Reproducibility

- Fixed seed 42
- Curated stream (deterministic)
- Config stored in config.json
- Raw results in results/exp_002/raw.csv

---

# Español

## Objetivo

Verificar H3 del Experimento 001: si la formación de cicatrices por
presión adaptativa detecta fallos raros pero graves que la formación
por repetición ignora.

---

## Diseño

En lugar de una distribución probabilística, el flujo es curado:

| Tipo de error            | Severidad | Impacto | Conteo |
|--------------------------|----------:|--------:|-------:|
| TRIVIAL_LOG_NOISE        | 0.10      | 0.10    | 25     |
| MODERATE_TIMEOUT         | 0.50      | 0.55    | 6      |
| SEVERE_DATA_CORRUPTION   | 0.95      | 0.99    | 1      |
| SEVERE_AUTH_BYPASS       | 0.90      | 0.95    | 2      |

Los eventos SEVERE ocurren solo 1 y 2 veces respectivamente — por debajo
del umbral de 3 exigido por la regla de repetición.

---

## Hipótesis

- A (Presión Adaptativa) forma cicatrices para SEVERE_DATA_CORRUPTION y
  SEVERE_AUTH_BYPASS porque su presión supera 0.55.
- B (Repetición) no forma cicatrices para ninguno, porque ninguno
  alcanza 3 repeticiones.

---

## Resultado Esperado

- Tasa de graves omitidos: A = 0.0, B = 1.0.
- Esto confirma que la formación por presión proporciona una propiedad
  de seguridad que la formación por repetición no puede ofrecer.

---

## Reproducibilidad

- Semilla fija 42
- Flujo curado (determinista)
- Configuración guardada en config.json
- Resultados crudos en results/exp_002/raw.csv
