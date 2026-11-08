"""Exact count verification (Tables 3 and 4) using the program's counted version."""
import csv
import math
import os
import random

from common import RESULTS, load_program
import formulas as F

prog = load_program()
key, pa, pb, pc, d = prog.variant_of(2023400213, 2023400039)
N_SAMPLES = 1000


def table3():
    rows = []
    for g in (1, 2, 3, 4):
        for n in (1, 5, 10, 20, 40, 100):
            cb = prog.algorithm_counted(list(F.best_input(g, n)), d)[1][g - 1]
            cw = prog.algorithm_counted(list(F.worst_input(g, n)), d)[1][g - 1]
            rows.append([g, n, cb, F.BEST[g - 1](n), cw, F.WORST[g - 1](n)])
    with open(os.path.join(RESULTS, "table3.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["group", "n", "counted_best", "formula_B", "counted_worst", "formula_W"])
        w.writerows(rows)
    bad = [r for r in rows if r[2] != r[3] or r[4] != r[5]]
    print("Table 3: %d rows, %d mismatches" % (len(rows), len(bad)))


def table4():
    seed = int.from_bytes(os.urandom(4), "big")
    rng = random.Random(seed)
    rows = []
    for n in (10, 40, 100):
        samples = [prog.algorithm_counted(prog.random_input(n, pa, pb, rng), d)[1] for _ in range(N_SAMPLES)]
        for g in (1, 2, 3, 4):
            vals = [c[g - 1] for c in samples]
            mean = sum(vals) / N_SAMPLES
            sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / (N_SAMPLES - 1))
            A = F.AVG[g - 1](n)
            rows.append([g, n, N_SAMPLES, mean, float(A), str(A), mean - float(A),
                         (mean - float(A)) / float(A), sd / math.sqrt(N_SAMPLES)])
    rows.sort()
    with open(os.path.join(RESULTS, "table4.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["group", "n", "N", "mean", "A_float", "A_exact", "diff", "rel_diff", "std_error", "seed"])
        for r in rows:
            w.writerow(r + [seed])
    for r in rows:
        print("g=%d n=%3d mean=%.4f A=%.4f diff=%+.4f (%.2f%%) se=%.4f z=%.2f" %
              (r[0], r[1], r[3], r[4], r[6], 100 * r[7], r[8], r[6] / r[8] if r[8] else 0))


if __name__ == "__main__":
    table3()
    table4()
