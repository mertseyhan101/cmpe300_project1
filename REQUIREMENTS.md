# REQUIREMENTS.md — CMPE 300 Project 1 master checklist

Authoritative source: `Cmpe300_Project1.pdf` (6 pages, the only version in the workspace,
modified 2026-11-07; image-based, so it was read from rendered pages, not text extraction).
Template: `report_tables.tex` / `report_tables.pdf`.

Status legend: Not started · In progress · Completed · Verified · Blocked · Requires student confirmation

## Decision log (interpretation of the assignment)

| # | Issue | Decision | Evidence |
|---|---|---|---|
| D1 | Variant parameters | key = (2023400213 + 2023400039) mod 8 = 4046800252 mod 8 = **4** → p_a = 2/5, p_b = 2/5, p_c = 1/5, **d = 2**. The task prompt said d = 3, but the PDF table (p. 2, row 4) says d = 2; the PDF wins. | Rendered p. 2 at 250 dpi |
| D2 | Which statements are in each group | (1) lines 3, 8; (2) lines 9, 15; (3) lines 4, 10, 14; (4) lines 7, 12, 16. Line 11 (`for r`), line 5, line 6 are **not** marked. | Rendered p. 2 |
| D3 | When a comparison is counted | A marked comparison counts once each time it is **evaluated**. Line 8 is evaluated only when line 3 is false. | Pseudocode semantics |
| D4 | "Loop increment" count | `for q ← 0 to s` ≡ `q ← 0; while q ≤ s: body; q ← q+1`, so the increment runs s+1 times (once per iteration). Likewise line 15 runs n−i increments. | Standard for-loop expansion |
| D5 | `while k > 0` iterations | k = n, n div d, … ; the body (line 7) runs ⌊log_d n⌋ + 1 times for n ≥ 1. | Proof in report §4 |
| D6 | Output format | One space after each colon, exactly `Variant: 4 (p_a=2/5, p_b=2/5, p_c=1/5, d=2)` and `Count(1): x Count(2): y Count(3): z Count(4): w`. | PDF §7 |
| D7 | Average-case run times | After each `Case: average …` line, print one indented line listing all individual run times. | PDF §7 ("also print the execution times of all the runs") |
| D8 | Small-n timing | A timing round repeats the same input until ≥ 20 ms has elapsed (at least once) and takes total/reps; each reported time is the minimum of 3 rounds (added after the first run showed 3–6× interference spikes; first run archived in `results/archive_first_attempt/`). Disclosed in report §10. | Timer resolution, desktop load |
| D9 | Asymptotic class of B2(n) = 0 | Written as O(1) (constant 0), since Θ needs an eventually positive function (Slide01 p. 26). | Slide01 |
| D11 | ReadMe per package | The ReadMe is generated per student so its commands name that package's `.py` file (audit finding: the shared ReadMe failed verbatim in 2023400039.zip). | Audit 2026-11-07 |
| D10 | WorkDone content | Drafts follow the proposed allocation and carry a DRAFT banner; must be confirmed/edited by each student. | Cannot verify personal contributions |

## Requirements

| ID | Section | Requirement / deliverable | Method | Verification | Status |
|---|---|---|---|---|---|
| R1 | §2 | Implement Algorithm 1 exactly (persistent `s`, floor division, all loops) | `src/2023400213.py::algorithm` | Exhaustive comparison vs. independent interpreter `tests/reference_interpreter.py`, n ≤ 8 | Verified |
| R2 | §2.1 | Compute and state key and parameters; Variant table in report | Program computes key from argv; report Variant table | Test + report | Verified |
| R3 | §2.1 | Final formulas for own parameters (general first allowed) | Derive with p_a,p_b,p_c,d then substitute | Fractions + sympy | Verified |
| R4 | §3 | 12 exact closed forms B/W/A for groups (1)–(4), no summations | Report §5–8 | Exhaustive (n ≤ 10), DP (n ≤ 120), exact expectation (n ≤ 9) | Verified |
| R5 | §3 | Asymptotic class for each of the 12 | Report, Θ proofs with explicit constants | Ratio checks | Verified |
| R6 | §3 | Explicit best/worst input of size n for each B/W | Report + `best_input/worst_input` | Counted = formula; exhaustive min/max | Verified |
| R7 | §3 | **Proof** that no input does fewer/more operations | Per-position bounds, pair-counting bound | Exhaustive + DP optimum | Verified |
| R8 | §3 | For every A(n): random variables, expectations, treatment of `s` | E[s_i] recurrence (Slide04 type 1) + indicators | Exact expectation by enumeration | Verified |
| R9 | §3 | Table 1 filled | `report/tables.tex` | Visual check | Verified |
| R10 | §4 | Identify "correct" basic operation and justify; comment on consistency | Report §10, timing vs counts | Correlation of time with each count | Verified |
| R11 | §4 | Code runs 15 sizes × {best, worst, average} = 45 times, uses best/worst of chosen op | Normal mode | CLI test, CSV | Verified |
| R12 | §4 | Average: random inputs by variant distribution, ≥ 10 runs per size | 10 runs | CSV has 10 runs per n | Verified |
| R13 | §4 | Table 2 filled + language + machine | Report | Values from `results/timing.csv` | Verified |
| R14 | §5 | One counter per group; counters not used while timing | Separate `algorithm` (no counters) and `algorithm_counted` | Code review + test | Verified |
| R15 | §5.1 | Table 3: n ∈ {1,5,10,20,40,100}, counted vs B/W formula, each group | `experiments/count_verification.py` | All equal | Verified |
| R16 | §5.2 | Table 4: n ∈ {10,40,100}, ≥ 1000 random inputs, mean vs A(n), comment on difference | N = 1000 | Difference explained (std. error) | Verified |
| R17 | §5 | Report mismatches honestly | n/a (none) | — | Verified |
| R18 | §6 | Graphs: x = n, y = complexity/time; cover all 12 analyses + actual times | `experiments/make_plots.py` | Figures in report | Verified |
| R19 | §6 | Comment on each of the 12 analyses vs actual time; compare average vs worst growth with pseudocode reasons | Report §12 | TA audit | Verified |
| R20 | §7 | ReadMe explaining how to run | `scripts/ReadMe.in`, rendered per student by `scripts/package.sh` | Every documented command executed literally from each extracted zip | Verified |
| R21 | §7 | Program takes 2 student numbers as args, prints variant first | CLI | subprocess tests | Verified |
| R22 | §7 | Normal mode lines `Case: <case> Size: <size> Elapsed Time (s): <time>` | CLI | Regex test | Verified |
| R23 | §7 | Print all run times for each average result | CLI (D7) | Test | Verified |
| R24 | §7 | Count mode: run once, print only variant line and Count line | CLI | subprocess tests incl. hidden-like inputs | Verified |
| R25 | §8 | Single LaTeX report including the 4 tables (layout/row/column order unchanged) | `report/main.tex` | Compile + visual inspection | Verified |
| R26 | §8 | Report contains derivations, proofs, basic op, count verification, graphs, comments | Report | TA audit | Verified |
| R27 | §8 | WorkDone document per student starting "I worked on the following parts in this project:", specific, not identical between students | `workdone/*.tex` | Drafts | **Requires student confirmation** |
| R28 | §8 | Files: StudentNumber.pdf, StudentNumber.py, ReadMe, StudentNumber_WorkDone.pdf in StudentNumber.zip, per student | `scripts/package.sh` | Extract + run | Verified (technical) — blocked on R27 |
| R29 | §8 | Deadline Fri 13 Nov 2026 23:59; upload to Moodle by students | Not automated | — | Students' action |
