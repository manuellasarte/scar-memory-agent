#!/usr/bin/env bash
#
# Reproduce all experiments and generate all results from scratch.
# Reproduce todos los experimentos y genera todos los resultados desde cero.
#
# Usage / Uso:
#   bash reproduce.sh
#

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "==> [0/8] Ensuring required directories exist"
mkdir -p data
mkdir -p paper/figures
mkdir -p results/exp_001
mkdir -p results/exp_002
mkdir -p results/exp_001_multiseed
mkdir -p results/joint

echo "==> [1/8] Cleaning previous outputs"
rm -f data/scar_memory.db
rm -f results/exp_001/*.json results/exp_001/*.csv results/exp_001/*.tex
rm -f results/exp_002/*.json results/exp_002/*.csv results/exp_002/*.tex
rm -f experiments/exp_001_pressure_vs_repetition/stream.json
rm -f experiments/exp_002_rare_severe/stream.json

echo "==> [2/8] Initializing database"
python3 -c "from src.db import init_db; init_db()"

echo "==> [3/8] Generating Experiment 001 stream"
python3 -m src.error_stream

echo "==> [4/8] Running Experiment 001 (adaptive pressure vs repetition)"
python3 -m src.run_experiment
python3 -m src.report_exp001

echo "==> [5/8] Generating Experiment 002 curated stream"
python3 -m src.error_stream_curated

echo "==> [6/8] Running Experiment 002 (rare severe failures)"
python3 -m src.run_experiment_002
python3 -m src.report_exp002

echo "==> Multi-seed robustness study (10 seeds)"
python3 -m src.multiseed_experiment

echo "==> [7/8] Generating figures"
python3 -m src.plot_results

echo "==> [8/8] Verifying results"
test -f results/exp_001/summary.json
test -f results/exp_001/deltas.json
test -f results/exp_001/table.tex
test -f results/exp_002/summary.json
test -f results/exp_002/deltas.json
test -f results/exp_002/table.tex
test -f paper/figures/results_comparison.png
test -f results/exp_001_multiseed/summary.json
test -f paper/tables/multiseed.tex

echo "==> Building PDF (optional, requires pandoc + lualatex)"
if command -v pandoc >/dev/null 2>&1 && command -v lualatex >/dev/null 2>&1; then
    bash build_pdf.sh || echo "WARN: PDF build failed (optional step)"
else
    echo "SKIP: pandoc or lualatex not installed"
fi

echo "==> Done"
echo ""
echo "All results regenerated:"
echo "  results/exp_001/"
echo "  results/exp_002/"
echo "  results/joint/joint_report.md"
