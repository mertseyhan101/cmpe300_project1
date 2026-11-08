# FINAL_VERIFICATION_REPORT.md

Date: 2026-11-07. Deadline in the assignment: Fri 13 Nov 2026 23:59.

## Status: technically complete; NOT ready to submit until both WorkDone documents are confirmed

## 1. Variant (verified from the rendered PDF, page 2)
key = (2023400213 + 2023400039) mod 8 = 4 → p_a = 2/5, p_b = 2/5, p_c = 1/5, **d = 2**.
The task prompt said d = 3; that is row 5 of the table, so it was not used.

## 2. Deliverables
| File | Purpose |
|---|---|
| `submission/2023400213.zip` | 2023400213.pdf, 2023400213.py, ReadMe, 2023400213_WorkDone.pdf |
| `submission/2023400039.zip` | 2023400039.pdf, 2023400039.py, ReadMe, 2023400039_WorkDone.pdf |
| `src/2023400213.py` | program (single source; the .py in both zips is this exact file) |
| `report/main.tex` → `report/main.pdf` | 22-page report |
| `workdone/*.tex` | WorkDone drafts (DRAFT banner on, controlled by `workdone/status.tex`) |
| `scripts/ReadMe.in` | ReadMe template; `package.sh` renders a student-specific `ReadMe` into each zip |
| `REQUIREMENTS.md`, `COURSE_METHODS.md`, `IMPLEMENTATION_PLAN.md` | checklist, lecture mapping, plan |
| `analysis/`, `tests/`, `experiments/`, `results/`, `figures/`, `scripts/` | verification, data, figures, build |

## 3. The twelve results (λ = ⌊log₂ n⌋ + 1)
| Group | B(n) | W(n) | A(n) |
|---|---|---|---|
| (1) | n, Θ(n) — aⁿ | 2n, Θ(n) — bⁿ | 8n/5, Θ(n) |
| (2) | 0, O(1) — aⁿ | n(n+1)/2, Θ(n²) — cⁿ | n²/10 + 13n/10 − 4 + 4(4/5)ⁿ, Θ(n²) |
| (3) | n, Θ(n) — aⁿ | n + ⌊n²/4⌋, Θ(n²) — a^⌊n/2⌋ b^⌈n/2⌉ | 9n/5 − 4 + 4(4/5)ⁿ, Θ(n) |
| (4) | nλ − λ(λ−1)/2, Θ(n log n) — a^(n−λ) c^λ | n⌊n²/4⌋ + n⌈n/2⌉ + ⌊n/2⌋λ, Θ(n³) — a^⌊n/2⌋ b^⌈n/2⌉ | 13n²/10 − 39n/10 + (2n/5)λ + 4n(4/5)ⁿ, Θ(n²) |

Key fact for A(n): E[s_i] = 2(1 − (4/5)^i) < 2, from E[s_{i+1}] = (4/5)E[s_i] + 2/5 (s_i is independent of arr[i]).
Correct basic operation: group (4).

## 4. Mathematical verification (`analysis/verify_math.py`, log in `results/math_verification.txt`): 0 failures
- Independent line-by-line interpreter, all 3ⁿ inputs, n = 1..10: min/max equal B/W, and the stated inputs attain them.
- Exact expectation with Fraction weights, n = 1..9: equal to A(n) (both the general and the simplified form).
- DP over (i, s), exact optimum over all 3ⁿ inputs, n = 1..120: equal to B/W.
- DP over the distribution of s, exact expectation, n = 1..40, 50, 60, 80, 100, 150: equal to A(n).
- Per-character cost model vs. interpreter on 300 random strings (n ≤ 60): equal.
- sympy: general A1..A4 reduce to the variant forms; leading constants A2/n² → 1/10, A4/n² → 13/10, W4/n³ → 1/4, B4/(n log₂ n) → 1.

## 5. Tests: `pytest tests` → 72 passed
Variant, hand-computed pseudocode cases (`abcabcba` → res 227, counts 13/14/10/61), s persistence/reset, floor
division, exhaustive vs. interpreter (all strings up to length 8, d = 2 and 3), formulas, exact enumeration of A(n),
CLI subprocess tests (count mode exact output, other variant, empty string, bad arguments, full normal-mode format),
random-input distribution, determinism.

## 6. Experiments
- Table 2: 45 timings + 150 individual average runs (`results/timing.csv`, `results/normal_mode_output.txt`).
  Machine: MacBook Air M1, 16 GB, macOS 15.5, CPython 3.14.3, `perf_counter`, min of 3 rounds of ≥ 20 ms.
  Measured worst time at n = 400: 0.64 s; average: 7.7 ms; best: 0.23 ms.
- Table 3: 48/48 counted values equal the formulas.
- Table 4: N = 1000 per n; all 12 differences < 2 standard errors (max |z| = 1.79, max |relative| = 1.9 %).
- Basic-operation choice: time per group-(4) operation 31–86 ns over 132 timed inputs (n ≥ 40); the other groups
  vary by 40× to 3113×.

## 7. Report / LaTeX
Compiled with Tectonic (installed via Homebrew). The only remaining warning is a non-UTF-8 byte in a comment inside
`algorithm.sty`, which does not affect the output. Pages were inspected visually: the tables keep the template's
layout, row order and column order, there are no clipped formulas, and all 5 figures render with captions.

## 8. ZIP validation (`scripts/package.sh`)
Each zip was extracted to a clean temporary directory and checked: exactly 4 files with the right names, both PDFs
open, count mode matches the expected output, normal mode prints the variant line plus 45 `Case:` lines. The program
also runs under the system Python 3.9.6.

## 9. Remaining items / honest caveats
1. **WorkDone documents (required before submission).** Both are drafts based on the proposed allocation. I can't
   confirm who actually did what. Each student must edit `workdone/<No>_WorkDone.tex` to describe their real work,
   set `workdone/status.tex` to `\draftfalse`, then run `scripts/build_all.sh && scripts/package.sh`.
2. **AI assistance.** The analysis, code and report were produced with an AI assistant (Claude Code). The updated
   assignment PDF does not prohibit this, but the WorkDone statements must be truthful, so the students should decide
   whether and how to state it.
3. **Timing noise.** Measurements were taken during normal desktop use (load average ≈ 3). This is disclosed in
   report §10/§12.4, and the noisy first run is archived. Rerunning gives different absolute times but the same
   growth rates.
4. The program prints timing values with 9 decimals. The PDF does not specify a precision.
5. Upload to Moodle is not automated; the students must do it.

## 10. Post-audit corrections (2026-11-07)
An independent read-only audit returned PASS WITH WARNINGS (no mathematical, code or data errors). Corrections:
- ReadMe: now generated per package, so the commands name `2023400213.py` or `2023400039.py`; the runtime is
  described as machine-dependent; tested versions are listed (Python 3.9.6, 3.12.1, 3.14.3).
  `package.sh` runs every documented command literally from each extracted zip.
- Report wording: §1 provenance sentence; ρ = 1 − p_c (no clash with loop variable q); §7.1 tie at n − i = λ;
  §8.1 DP scope; §12.2 empirical slopes stated as approximate, with a real re-run
  (`results/rerun_2026-11-07_normal_mode_output.txt`) quoted; "nearly flat" replaced. Layout: stats table kept with
  its paragraph, no near-empty pages (22 pages).
- WorkDone drafts: invented cross-check details replaced by red `[STUDENT TO FILL IN]` placeholders; the banner now
  also asks the students to state AI assistance where relevant. `package.sh` refuses final packaging while a
  placeholder remains and draft mode is off.
- No change to the algorithm, counters, formulas, tables, data or figures.
