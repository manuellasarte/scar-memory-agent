# Results — Experiment 001

# English

## Setup

Two agents were exposed to the same synthetic stream of 500 failure events,
generated with a fixed seed (42). Agent A uses adaptive-pressure scar
formation (threshold = 0.55). Agent B uses a repetition rule
(3 identical failures → scar). The only difference between agents is the
scar formation mechanism.

## Summary Table

| Metric              | Adaptive Pressure (A) | Repetition (B) |
|---------------------|----------------------:|---------------:|
| Scars formed        | 2                     | 3              |
| Capabilities born   | 2                     | 3              |
| Avg utility score   | 0.7500                | 0.5778         |
| Survival rate       | 1.0000                | 0.6667         |
| False scar rate     | 0.0000                | 0.3333         |
| Missed severe rate  | 0.0000                | 0.0000         |

## Findings

- H1 confirmed: adaptive-pressure formation achieved a 29.8 % higher
  average capability utility than repetition-based formation.
- H2 confirmed: adaptive-pressure formation produced zero false-positive
  scars, while repetition produced one scar from TRIVIAL events.
- H3 not confirmed in this stream: SEVERE events occurred more than three
  times each, so the repetition rule also detected them. This is a
  limitation of the current synthetic stream and motivates Experiment 002.

## Interpretation

The mechanism does not "count errors". It measures cumulative adaptive
pressure combining frequency, severity, and impact. This distinction is
what allows the system to ignore recurring trivial failures while still
responding to high-pressure failures.

## Limitations

- Synthetic stream; real-world failure distributions may differ.
- Only one seed was used in this run.
- The utility model (TRUE_VALUE per error type) is a declared modeling
  assumption, not an empirical measurement.

---

# Español

## Configuración

Dos agentes fueron expuestos al mismo flujo sintético de 500 eventos
de fallo, generado con semilla fija (42). El Agente A usa formación
de cicatrices por presión adaptativa (umbral = 0.55). El Agente B usa
una regla de repetición (3 fallos idénticos → cicatriz). La única
diferencia entre agentes es el mecanismo de formación de cicatrices.

## Tabla Resumen

| Métrica              | Presión Adaptativa (A) | Repetición (B) |
|----------------------|-----------------------:|---------------:|
| Cicatrices formadas  | 2                      | 3              |
| Capacidades nacidas  | 2                      | 3              |
| Utilidad promedio    | 0.7500                 | 0.5778         |
| Tasa de supervivencia| 1.0000                 | 0.6667         |
| Tasa de falsas       | 0.0000                 | 0.3333         |
| Tasa de omitidas     | 0.0000                 | 0.0000         |

## Hallazgos

- H1 confirmada: la formación por presión adaptativa logró un 29.8 %
  más de utilidad promedio por capacidad que la formación por repetición.
- H2 confirmada: la formación por presión produjo cero cicatrices falsas,
  mientras que la repetición produjo una cicatriz a partir de eventos TRIVIAL.
- H3 no confirmada en este flujo: los eventos SEVERE aparecieron más de
  tres veces cada uno, por lo que la regla de repetición también los detectó.
  Esto es una limitación del flujo sintético actual y motiva el Experimento 002.

## Interpretación

El mecanismo no "cuenta errores". Mide presión adaptativa acumulada
combinando frecuencia, severidad e impacto. Esa distinción es lo que
permite ignorar fallos triviales recurrentes mientras se responde a
fallos de alta presión.

## Limitaciones

- Flujo sintético; las distribuciones reales pueden diferir.
- Solo se usó una semilla en esta ejecución.
- El modelo de utilidad (TRUE_VALUE por tipo de error) es una asunción
  de modelado declarada, no una medición empírica.
