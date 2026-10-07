# Changelog

## [Fase 7] — High-impact refinements
- 7.1 Data figure (`paper/figures/results_comparison.png` + `.svg`)
- 7.2 Multi-seed robustness study (10 seeds)
- 7.3 PDF compilation (`build_pdf.sh`, `paper/paper.pdf`)
- Added `paper/tables/multiseed.tex`
- Added `src/plot_results.py`
- Added `src/multiseed_experiment.py`
- Sections 5.4 and 5.5 added (EN + ES)

## [Fase 6.2] — Reproducibility and project packaging
- Added `reproduce.sh` (single-command reproducibility)
- Added `.gitignore`
- Added root `README.md` (bilingual)
- Added `LICENSE` (MIT)
- Extended reporting for Experiment 002
- Cleaned obsolete backups and caches

## [Fase 5] — Full paper completed
- Paper complete in EN + ES (1046 lines)
- 8 sections + abstract + reproducibility statement

## [Fase 4] — Paper synthesis
- Tables (main_results.tex, deltas.tex)
- Figure (pipeline.mmd + pipeline.txt)
- Results section, Discussion, Limitations

## [Fase 4.5] — Discussion and Limitations
- Wrote Discussion section (EN/ES)
- Wrote Limitations section (EN/ES)
- Added `paper/limitations.md` as standalone document
- Updated paper to Draft v0.5

## [Fase 4.4] — Results section
- Wrote full Results section (EN/ES)
- Added `paper/paper.md` (Draft v0.4)
- Added `paper/includes.md` with cross-references

## [Fase 4.3] — Conceptual figure
- Added `paper/figures/pipeline.mmd`
- Added `paper/figures/pipeline.txt`
- Added `paper/figures/README.md`

## [Fase 4.2] — Unified LaTeX tables
- Added `paper/tables/main_results.tex`
- Added `paper/tables/deltas.tex`
- Added `paper/tables/README.md`

## [Fase 4.1] — Joint report
- Added `results/joint/joint_report.md`

# English

## [Fase 2.5] — Experiment 001 analysis
- Added `paper/results_exp001.md` (bilingual)
- Added `paper/results_exp001.tex`
- Confirmed H1 and H2
- Recognized limitation for H3 (SEVERE events repeated in current stream)
- Motivated Experiment 002 with rare isolated SEVERE events

## [Fase 2.4] — Results consolidated
- Normalized `scar_pressure` in Agent B to [0,1]
- Added `src/report_exp001.py`
- Generated `deltas.json`, `table.tex`, `results/exp_001/README.md`

## [Fase 2.3] — Dual execution
- Added `src/agent_adaptive_pressure.py`
- Added `src/agent_repetition.py`
- Added `src/run_experiment.py`

## [Fase 2.2] — Error stream
- Added `src/error_stream.py`
- Added `experiments/exp_001_pressure_vs_repetition/config.json`
- Added generated `stream.json`

## [Fase 2.1] — Experiment design
- Added `experiments/exp_001_pressure_vs_repetition/README.md`

---

# Español

## [Fase 2.5] — Análisis del Experimento 001
- Añadido `paper/results_exp001.md` (bilingüe)
- Añadido `paper/results_exp001.tex`
- Confirmadas H1 y H2
- Reconocida limitación en H3 (los eventos SEVERE se repiten en el flujo actual)
- Motivado el Experimento 002 con eventos SEVERE raros y aislados

## [Fase 2.4] — Resultados consolidados
- Normalizada `scar_pressure` en el Agente B a [0,1]
- Añadido `src/report_exp001.py`
- Generados `deltas.json`, `table.tex`, `results/exp_001/README.md`

## [Fase 2.3] — Ejecución dual
- Añadido `src/agent_adaptive_pressure.py`
- Añadido `src/agent_repetition.py`
- Añadido `src/run_experiment.py`

## [Fase 2.2] — Flujo de errores
- Añadido `src/error_stream.py`
- Añadido `experiments/exp_001_pressure_vs_repetition/config.json`
- Añadido `stream.json` generado

## [Fase 2.1] — Diseño experimental
- Añadido `experiments/exp_001_pressure_vs_repetition/README.md`
