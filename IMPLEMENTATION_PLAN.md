# IMPLEMENTATION_PLAN.md

## Directory layout

```
src/2023400213.py          submitted program (single file, stdlib only); copied to 2023400039.py at packaging
analysis/formulas.py       closed-form formulas (exact Fractions), written independently of the program
analysis/verify_math.py    exhaustive / DP / exact-expectation / sympy verification -> results/math_verification.txt
tests/reference_interpreter.py  independent line-by-line interpreter of Algorithm 1 (own counters)
tests/test_*.py            pytest suite (variant, pseudocode, exhaustive, math, CLI, reliability)
experiments/run_timing.py        45 timings (+10 runs per average) -> results/timing.csv, results/timing_runs.csv
experiments/count_verification.py Tables 3 & 4 -> results/table3.csv, results/table4.csv
experiments/make_plots.py         figures/*.pdf
experiments/make_tables.py        report/generated/*.tex from the CSVs (no hand-typed numbers)
report/main.tex            full report (includes the official tables)
workdone/*.tex             WorkDone drafts
scripts/build_all.sh       run everything; scripts/package.sh builds and validates the zips
```

## Tasks and dependencies

| # | Task | Depends on | Output |
|---|---|---|---|
| 1 | Pseudocode interpretation (D2–D5 in REQUIREMENTS.md) | — | decision log |
| 2 | Per-character cost table (what one iteration costs for a/b/c given s) | 1 | basis of all 12 analyses |
| 3 | Derive 12 closed forms + proofs (general p, d, then key 4) | 2 | analysis notes → report |
| 4 | Independent reference interpreter | 1 | tests/reference_interpreter.py |
| 5 | Program: algorithm (no counters), counted version, generators, timing, CLI | 1 | src/2023400213.py |
| 6 | Formula module + math verification (exhaustive, DP, exact E, sympy) | 3, 4 | results/math_verification.txt |
| 7 | Test suite | 4, 5, 6 | pytest pass |
| 8 | Choose "correct" basic op (theory + time/count correlation) | 3, 5 | report §10 |
| 9 | Timing experiment (45 + raw runs) | 5, 8 | results/timing*.csv |
| 10 | Count verification Tables 3/4 | 5, 6 | results/table3/4.csv |
| 11 | Graphs | 6, 9, 10 | figures/ |
| 12 | Tables in LaTeX generated from CSV | 9, 10 | report/generated |
| 13 | Report writing + compile + visual check | 3, 11, 12 | report/main.pdf |
| 14 | ReadMe, WorkDone drafts | 5, 13 | ReadMe, workdone/*.pdf |
| 15 | Packaging + validation from extracted zip | 13, 14 | submission/*.zip |
| 16 | Final TA-style audit, FINAL_VERIFICATION_REPORT.md | all | — |

## Independence of verification

* The reference interpreter is written as an explicit line-by-line simulation (explicit while-loop
  expansion of every `for`, explicit k loop) with its own counters; it does not import the program.
* Formulas in `analysis/formulas.py` are written from the derivation, not from the program.
* Best/worst optimality is checked three ways: exhaustive search over all 3^n strings (n ≤ 10),
  an exact dynamic program over (position, s) for n ≤ 120 (does not rely on the proof), and the proof itself.
* A(n) is checked by exact enumeration with Fraction weights (n ≤ 9), by an exact DP over the
  distribution of s (n ≤ 150), by sympy simplification of the general formula, and by Monte Carlo (Table 4).
