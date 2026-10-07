#!/usr/bin/env bash
#
# Compile paper/paper.md to paper/paper.pdf
# Compila paper/paper.md a paper/paper.pdf
#

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

OUT="paper/paper.pdf"

echo "==> Building $OUT with lualatex"

pandoc paper/paper.md \
    -o "$OUT" \
    --pdf-engine=lualatex \
    --toc \
    --toc-depth=3 \
    --number-sections \
    -V geometry:margin=2.5cm \
    -V fontsize=11pt \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue \
    -V documentclass=article \
    --resource-path=paper \
    2>&1 | tail -20

if [ -f "$OUT" ]; then
    echo "OK -> $OUT"
    ls -la "$OUT"
else
    echo "FAIL: PDF not created"
    exit 1
fi
