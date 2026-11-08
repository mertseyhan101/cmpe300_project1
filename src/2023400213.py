#!/usr/bin/env python3
"""CMPE 300 - Project 1.

Implementation of Algorithm 1 ("Example Algorithm") with
  * a plain version used for timing (no counters),
  * a counted version with one counter per basic-operation group (1)-(4),
  * best / worst / average input generators,
  * the timing experiment (normal mode) and the count mode.

Usage:
    python3 2023400213.py <No1> <No2>                    # timing experiment
    python3 2023400213.py <No1> <No2> --count <string>   # count mode

Only the Python standard library is used.
"""

import gc
import random
import sys
import time
from fractions import Fraction

# ---------------------------------------------------------------------------
# Variant table (Section 2.1 of the project description)
# key: (p_a, p_b, p_c, d)
# ---------------------------------------------------------------------------
VARIANTS = {
    0: (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), 2),
    1: (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), 3),
    2: (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), 2),
    3: (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), 3),
    4: (Fraction(2, 5), Fraction(2, 5), Fraction(1, 5), 2),
    5: (Fraction(2, 5), Fraction(2, 5), Fraction(1, 5), 3),
    6: (Fraction(1, 6), Fraction(1, 2), Fraction(1, 3), 2),
    7: (Fraction(1, 6), Fraction(1, 2), Fraction(1, 3), 3),
}

SIZES = [1, 5, 10, 20, 40, 50, 60, 80, 100, 150, 200, 250, 300, 350, 400]
AVERAGE_RUNS = 10          # random inputs per size for the average case
MIN_TIMED_SECONDS = 0.02   # one timing round repeats the input until this much time has passed
TIMING_ROUNDS = 3          # rounds per timed run; the fastest round is reported


def variant_of(no1, no2):
    """Return (key, p_a, p_b, p_c, d) for the two student numbers."""
    key = (no1 + no2) % 8
    p_a, p_b, p_c, d = VARIANTS[key]
    return key, p_a, p_b, p_c, d


def variant_line(key, p_a, p_b, p_c, d):
    return "Variant: {} (p_a={}, p_b={}, p_c={}, d={})".format(key, p_a, p_b, p_c, d)


# ---------------------------------------------------------------------------
# Algorithm 1 -- plain version (used for timing, no counters)
# ---------------------------------------------------------------------------
def algorithm(arr, d):
    n = len(arr)
    res = 0
    s = 0                                   # line 1 (s is NOT reset per iteration)
    for i in range(0, n):                   # line 2:  i = 0 .. n-1
        if arr[i] == 'a':                   # line 3
            s = s + 1                       # line 4
            k = n                           # line 5
            while k > 0:                    # line 6
                k = k // d                  # line 7:  k = floor(k/d)
        elif arr[i] == 'b':                 # line 8
            for q in range(0, s + 1):       # line 9:  q = 0 .. s
                res = res + q               # line 10
                for r in range(1, n + 1):   # line 11: r = 1 .. n
                    res = res + r           # line 12
        else:                               # line 13: arr[i] = 'c'
            s = 0                           # line 14
            for t in range(i, n):           # line 15: t = i .. n-1
                res = res + t               # line 16
    return res                              # line 17


# ---------------------------------------------------------------------------
# Algorithm 1 -- counted version (used only for exact count verification)
# ---------------------------------------------------------------------------
def algorithm_counted(arr, d):
    """Run Algorithm 1 once and return (res, [c1, c2, c3, c4]).

    c1: comparisons on lines 3 and 8 (each counted when it is evaluated)
    c2: loop increments of the loops on lines 9 and 15 (one per iteration)
    c3: assignments on lines 4, 10, 14
    c4: assignments on lines 7, 12, 16
    """
    n = len(arr)
    c1 = c2 = c3 = c4 = 0
    res = 0
    s = 0
    for i in range(0, n):
        c1 += 1                             # line 3 comparison is always evaluated
        if arr[i] == 'a':
            s = s + 1
            c3 += 1                         # line 4
            k = n
            while k > 0:
                k = k // d
                c4 += 1                     # line 7
        else:
            c1 += 1                         # line 8 comparison (line 3 was false)
            if arr[i] == 'b':
                for q in range(0, s + 1):
                    c2 += 1                 # line 9 increment
                    res = res + q
                    c3 += 1                 # line 10
                    for r in range(1, n + 1):
                        res = res + r
                        c4 += 1             # line 12
            else:
                s = 0
                c3 += 1                     # line 14
                for t in range(i, n):
                    c2 += 1                 # line 15 increment
                    res = res + t
                    c4 += 1                 # line 16
    return res, [c1, c2, c3, c4]


# ---------------------------------------------------------------------------
# Input generators.  The "correct" basic operation is group (4) (the innermost
# assignments); its best- and worst-case inputs are used for timing.
# ---------------------------------------------------------------------------
def log_steps(n, d):
    """Number of iterations of 'while k > 0: k = k // d' starting from k = n."""
    steps = 0
    k = n
    while k > 0:
        k //= d
        steps += 1
    return steps


def best_input(n, d):
    """Best case of group (4): a^(n-L) c^L with L = floor(log_d n) + 1."""
    L = log_steps(n, d)
    return ['a'] * (n - L) + ['c'] * L


def worst_input(n, d):
    """Worst case of group (4): a^floor(n/2) b^ceil(n/2)."""
    return ['a'] * (n // 2) + ['b'] * (n - n // 2)


def random_input(n, p_a, p_b, rng=random):
    """Each position independently: 'a' w.p. p_a, 'b' w.p. p_b, 'c' otherwise."""
    pa = float(p_a)
    pab = float(p_a + p_b)
    arr = []
    for _ in range(n):
        u = rng.random()
        if u < pa:
            arr.append('a')
        elif u < pab:
            arr.append('b')
        else:
            arr.append('c')
    return arr


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------
def time_run(arr, d):
    """Elapsed time (s) of one execution of the algorithm on arr.

    Very small inputs finish in a few microseconds, so within one round the same
    input is executed repeatedly until at least MIN_TIMED_SECONDS have passed and
    the mean time per execution is taken. This is done in TIMING_ROUNDS rounds and
    the smallest round mean is returned (the usual timeit practice: larger values
    are caused by other processes, not by the algorithm). Input generation is
    outside the timed region and the garbage collector is disabled while timing.
    """
    gc_was_enabled = gc.isenabled()
    gc.disable()
    try:
        best = None
        for _ in range(TIMING_ROUNDS):
            reps = 0
            start = time.perf_counter()
            while True:
                algorithm(arr, d)
                reps += 1
                elapsed = time.perf_counter() - start
                if elapsed >= MIN_TIMED_SECONDS:
                    break
            per_run = elapsed / reps
            if best is None or per_run < best:
                best = per_run
    finally:
        if gc_was_enabled:
            gc.enable()
    return best


def run_experiment(p_a, p_b, d, sizes=SIZES, runs=AVERAGE_RUNS, rng=random, out=sys.stdout):
    """Print the 45 timing results; return a list of rows for optional CSV export."""
    rows = []
    for case in ("best", "worst"):
        for n in sizes:
            arr = best_input(n, d) if case == "best" else worst_input(n, d)
            t = time_run(arr, d)
            rows.append((case, n, 0, t))
            print("Case: {} Size: {} Elapsed Time (s): {:.9f}".format(case, n, t), file=out)
    for n in sizes:
        times = []
        for run in range(runs):
            arr = random_input(n, p_a, p_b, rng)
            t = time_run(arr, d)
            times.append(t)
            rows.append(("average_run", n, run + 1, t))
        mean = sum(times) / len(times)
        rows.append(("average", n, 0, mean))
        print("Case: average Size: {} Elapsed Time (s): {:.9f}".format(n, mean), file=out)
        print("    Runs (s): " + ", ".join("{:.9f}".format(t) for t in times), file=out)
    return rows


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------
USAGE = ("usage: python3 {0} <No1> <No2>\n"
         "       python3 {0} <No1> <No2> --count <string>")


def main(argv):
    prog = argv[0] if argv else "StudentNumber.py"
    args = argv[1:]
    if len(args) not in (2, 4) or (len(args) == 4 and args[2] != "--count"):
        print(USAGE.format(prog), file=sys.stderr)
        return 2
    try:
        no1, no2 = int(args[0]), int(args[1])
    except ValueError:
        print("error: student numbers must be integers", file=sys.stderr)
        return 2

    key, p_a, p_b, p_c, d = variant_of(no1, no2)

    if len(args) == 4:                                   # count mode
        text = args[3]
        if any(ch not in "abc" for ch in text):
            print("error: the input string may contain only a, b and c", file=sys.stderr)
            return 2
        _, counts = algorithm_counted(list(text), d)
        print(variant_line(key, p_a, p_b, p_c, d))
        print("Count(1): {} Count(2): {} Count(3): {} Count(4): {}".format(*counts))
        return 0

    print(variant_line(key, p_a, p_b, p_c, d))           # normal mode
    sys.stdout.flush()
    run_experiment(p_a, p_b, d)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
