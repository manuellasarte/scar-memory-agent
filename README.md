# Scar Memory Agent

**Adaptive-pressure scar formation for emergent capabilities**

---

# English

## What is this?

A mechanism by which an autonomous agent transforms recurring failures
into persistent capabilities through the formation of "scars". Unlike
repetition-based approaches, scar formation here is driven by *adaptive
pressure* -- a weighted combination of failure frequency, severity, and
impact.

The full paper is at `paper/paper.md`.

## Quick start

    git clone <repo-url>
    cd scar-memory-agent
    bash reproduce.sh

That single command regenerates every table, figure, and result in the
paper from scratch.

## Key results

Two complementary experiments compare adaptive-pressure formation
(Agent A) against a repetition-based baseline (Agent B).

| Experiment          | Metric             | A      | B      |
|---------------------|--------------------|--------|--------|
| 001 (probabilistic) | Avg utility        | 0.7500 | 0.5778 |
| 001 (probabilistic) | Survival rate      | 1.0000 | 0.6667 |
| 001 (probabilistic) | False scar rate    | 0.0000 | 0.3333 |
| 002 (rare severe)   | Missed severe rate | 0.0000 | 1.0000 |

- **+29.8%** average utility (Exp 001)
- **+50.0%** survival rate (Exp 001)
- **+115.1%** average utility (Exp 002)
- **100%** of rare severe failures detected (Exp 002), vs **0%** baseline

## Repository layout

    src/              Python implementation
    experiments/      Experiment configs and generated streams
    results/          Metrics, deltas, and LaTeX tables per experiment
    docs/             Design documents
    paper/            Full paper (Markdown + LaTeX tables + figures)
    data/             SQLite database (regenerated)
    reproduce.sh      Single-command reproduction script

## Requirements

- Python 3.10+
- SQLite3 (bundled with Python)
- Optional: pdflatex for compiling the LaTeX tables

No external Python packages are required.

## License

MIT -- see `LICENSE`.


---

# Espanol

## Que es esto?

Un mecanismo mediante el cual un agente autonomo transforma fallos
recurrentes en capacidades persistentes a traves de la formacion de
"cicatrices". A diferencia de los enfoques basados en repeticion, la
formacion de cicatrices aqui esta guiada por *presion adaptativa* --
una combinacion ponderada de frecuencia, severidad e impacto.

El paper completo esta en `paper/paper.md`.

## Inicio rapido

    git clone <repo-url>
    cd scar-memory-agent
    bash reproduce.sh

Ese unico comando regenera cada tabla, figura y resultado del paper
desde cero.

## Resultados clave

Dos experimentos complementarios comparan la formacion por presion
adaptativa (Agente A) frente a una linea base de repeticion (Agente B).

| Experimento          | Metrica            | A      | B      |
|----------------------|--------------------|--------|--------|
| 001 (probabilistico) | Utilidad promedio  | 0.7500 | 0.5778 |
| 001 (probabilistico) | Supervivencia      | 1.0000 | 0.6667 |
| 001 (probabilistico) | Tasa de falsas     | 0.0000 | 0.3333 |
| 002 (graves raros)   | Graves omitidos    | 0.0000 | 1.0000 |

- **+29.8%** de utilidad promedio (Exp 001)
- **+50.0%** de supervivencia (Exp 001)
- **+115.1%** de utilidad promedio (Exp 002)
- **100%** de fallos graves raros detectados (Exp 002), vs **0%** baseline

## Estructura

    src/              Implementacion Python
    experiments/      Configuraciones y flujos generados
    results/          Metricas, deltas y tablas LaTeX por experimento
    docs/             Documentos de diseno
    paper/            Paper completo
    data/             Base de datos SQLite (regenerable)
    reproduce.sh      Script de reproduccion

## Requisitos

- Python 3.10+
- SQLite3 (incluido en Python)
- Opcional: pdflatex para compilar las tablas LaTeX

## Licencia

MIT -- ver `LICENSE`.
