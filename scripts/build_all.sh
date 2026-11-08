#!/bin/bash
# Rebuild everything from scratch: verification, experiments, figures, tables, PDFs.
#   scripts/build_all.sh            (keeps existing timing/count data)
#   scripts/build_all.sh --rerun    (also reruns the timing and count experiments)
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/bin/python
$PY analysis/verify_math.py > /dev/null
$PY -m pytest -q tests
if [[ "${1:-}" == "--rerun" ]]; then
  $PY experiments/run_timing.py > results/run_timing_stdout.txt
  $PY experiments/count_verification.py
fi
$PY experiments/summary_stats.py > /dev/null
$PY experiments/make_plots.py > /dev/null
$PY experiments/make_tables.py
(cd report && tectonic -X compile main.tex)
(cd workdone && tectonic -X compile 2023400213_WorkDone.tex && tectonic -X compile 2023400039_WorkDone.tex)
echo "build complete"
