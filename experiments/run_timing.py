"""Real execution experiment (Table 2) + evidence for the choice of basic operation.

Uses the submitted program's own functions (algorithm without counters, generators,
time_run). The counted version is run only AFTER timing, on the same inputs.
Outputs:
  results/normal_mode_output.txt  exactly what the program prints in normal mode
  results/timing.csv              case,n,run,seconds,c1,c2,c3,c4   (45 results + 150 average runs)
  results/machine.txt             language / machine information
  results/extremes_timing.csv     time of each group's own best/worst input (n = 100..400)
"""
import csv
import io
import os
import platform
import random
import subprocess
import sys

from common import RESULTS, load_program
import formulas as F

prog = load_program()
key, pa, pb, pc, d = prog.variant_of(2023400213, 2023400039)
seed = int.from_bytes(os.urandom(4), "big")
rng = random.Random(seed)


class Tee(io.StringIO):
    def write(self, s):
        sys.stdout.write(s)
        return super().write(s)


def machine_info():
    def sh(cmd):
        try:
            return subprocess.check_output(cmd, shell=True, text=True).strip()
        except Exception:
            return "n/a"
    return {
        "python": platform.python_implementation() + " " + platform.python_version(),
        "os": platform.platform(),
        "cpu": sh("sysctl -n machdep.cpu.brand_string"),
        "cores": sh("sysctl -n hw.ncpu"),
        "memory_bytes": sh("sysctl -n hw.memsize"),
        "model": sh("sysctl -n hw.model"),
        "timer": "time.perf_counter() (monotonic, resolution %s s)" % __import__("time").get_clock_info("perf_counter").resolution,
        "min_timed_seconds_per_round": prog.MIN_TIMED_SECONDS,
        "timing_rounds_per_run (min reported)": prog.TIMING_ROUNDS,
        "random_seed": seed,
    }


def main():
    info = machine_info()
    with open(os.path.join(RESULTS, "machine.txt"), "w") as fh:
        for k, v in info.items():
            fh.write("%s: %s\n" % (k, v))
    out = Tee()
    out.write(prog.variant_line(key, pa, pb, pc, d) + "\n")
    rows = []
    # Same procedure as normal mode, but keep the inputs to count them afterwards.
    for case in ("best", "worst"):
        for n in prog.SIZES:
            arr = prog.best_input(n, d) if case == "best" else prog.worst_input(n, d)
            t = prog.time_run(arr, d)
            rows.append([case, n, 0, t, arr])
            out.write("Case: {} Size: {} Elapsed Time (s): {:.9f}\n".format(case, n, t))
    for n in prog.SIZES:
        times = []
        for r in range(prog.AVERAGE_RUNS):
            arr = prog.random_input(n, pa, pb, rng)
            t = prog.time_run(arr, d)
            times.append(t)
            rows.append(["average_run", n, r + 1, t, arr])
        mean = sum(times) / len(times)
        rows.append(["average", n, 0, mean, None])
        out.write("Case: average Size: {} Elapsed Time (s): {:.9f}\n".format(n, mean))
        out.write("    Runs (s): " + ", ".join("{:.9f}".format(t) for t in times) + "\n")
    with open(os.path.join(RESULTS, "normal_mode_output.txt"), "w") as fh:
        fh.write(out.getvalue())
    with open(os.path.join(RESULTS, "timing.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case", "n", "run", "seconds", "c1", "c2", "c3", "c4", "input"])
        for case, n, r, t, arr in rows:
            if arr is None:
                w.writerow([case, n, r, repr(t), "", "", "", "", ""])
            else:
                c = prog.algorithm_counted(arr, d)[1]       # counting AFTER timing
                w.writerow([case, n, r, repr(t)] + c + ["".join(arr)])

    # Each group's own extreme inputs: does the count predict the time?
    with open(os.path.join(RESULTS, "extremes_timing.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["group", "kind", "n", "input_desc", "seconds", "c1", "c2", "c3", "c4"])
        desc = {("best", 1): "a^n", ("best", 2): "a^n", ("best", 3): "a^n", ("best", 4): "a^(n-L)c^L",
                ("worst", 1): "b^n", ("worst", 2): "c^n", ("worst", 3): "a^(n/2)b^(n/2)", ("worst", 4): "a^(n/2)b^(n/2)"}
        for n in (100, 200, 300, 400):
            for g in (1, 2, 3, 4):
                for kind in ("best", "worst"):
                    s = F.best_input(g, n) if kind == "best" else F.worst_input(g, n)
                    t = prog.time_run(list(s), d)
                    c = prog.algorithm_counted(list(s), d)[1]
                    w.writerow([g, kind, n, desc[(kind, g)], repr(t)] + c)
                    print("extreme g=%d %s n=%d t=%.6f counts=%s" % (g, kind, n, t, c))


if __name__ == "__main__":
    main()
