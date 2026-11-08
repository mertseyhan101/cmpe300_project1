"""Figures for the report, generated only from formulas and results/*.csv."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import FIGURES, RESULTS
import formulas as F

COL = {"best": "#2a78d6", "worst": "#eb6834", "average": "#1baf7a"}
MK = {"best": "o", "worst": "s", "average": "^"}
LS = {"best": "-", "worst": "--", "average": ":"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
    "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "lines.linewidth": 1.6, "lines.markersize": 4, "savefig.bbox": "tight",
})
CASES = ("best", "worst", "average")
SIZES = [1, 5, 10, 20, 40, 50, 60, 80, 100, 150, 200, 250, 300, 350, 400]
NS = list(range(1, 401))
NAMES = {1: "(1) comparisons", 2: "(2) loop increments", 3: "(3) assignments", 4: "(4) assignments"}


def theo(g, case, n):
    return float({"best": F.BEST, "worst": F.WORST, "average": F.AVG}[case][g - 1](n))


def load_times():
    t = {c: {} for c in CASES}
    for r in csv.DictReader(open(os.path.join(RESULTS, "timing.csv"))):
        if r["case"] in CASES:
            t[r["case"]][int(r["n"])] = float(r["seconds"])
    return t


def save(fig, name):
    fig.savefig(os.path.join(FIGURES, name))
    plt.close(fig)


def fig_theory():
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.4))
    for ax, g in zip(axes.flat, (1, 2, 3, 4)):
        for c in CASES:
            ys = [theo(g, c, n) for n in NS]
            ax.plot(NS, ys, LS[c], color=COL[c], label={"best": "B", "worst": "W", "average": "A"}[c] + "%d(n)" % g)
        ax.set_title(NAMES[g], color=INK, fontsize=9.5)
        ax.set_xlabel("input size n")
        ax.set_ylabel("number of operations")
        if g in (3, 4):
            ax.set_yscale("log")
            ax.set_ylabel("number of operations (log scale)")
        ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, "theory_counts.pdf")


def fig_times(t):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    for c in CASES:
        xs = SIZES
        ys = [t[c][n] for n in xs]
        axes[0].plot(xs, ys, LS[c], marker=MK[c], color=COL[c], label=c)
        axes[1].loglog(xs, ys, LS[c], marker=MK[c], color=COL[c], label=c)
    axes[0].set_title("Measured time (linear scale)", fontsize=9.5)
    axes[1].set_title("Measured time (log-log scale)", fontsize=9.5)
    for ax in axes:
        ax.set_xlabel("input size n")
        ax.set_ylabel("elapsed time (s)")
        ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, "measured_times.pdf")


def fit_alpha(times, counts):
    """least squares for time = alpha * count over n >= 40 (relative error weighting)."""
    pairs = [(tt, cc) for tt, cc in zip(times, counts) if cc > 0]
    return sum(tt / cc for tt, cc in pairs) / len(pairs)


def fig_theory_vs_time(t):
    """For group 4: measured time vs alpha * count, alpha fitted per case (s per operation)."""
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7))
    alphas = {}
    for ax, c in zip(axes, CASES):
        big = [n for n in SIZES if n >= 40]
        a = fit_alpha([t[c][n] for n in big], [theo(4, c, n) for n in big])
        alphas[c] = a
        ax.plot(NS, [a * theo(4, c, n) for n in NS], "-", color=INK2, linewidth=1.0,
                label="%.0f ns x %s4(n)" % (a * 1e9, {"best": "B", "worst": "W", "average": "A"}[c]))
        ax.plot(SIZES, [t[c][n] for n in SIZES], "none", marker=MK[c], color=COL[c], label="measured")
        ax.set_title(c + " case", fontsize=9.5)
        ax.set_xlabel("input size n")
        ax.set_ylabel("time (s)")
        ax.legend(loc="upper left", fontsize=7.5)
    fig.tight_layout()
    save(fig, "group4_fit.pdf")
    with open(os.path.join(RESULTS, "group4_alpha.csv"), "w") as fh:
        fh.write("case,alpha_seconds_per_op\n")
        for c, a in alphas.items():
            fh.write("%s,%r\n" % (c, a))


def fig_ratio(t):
    """Measured time / theoretical count for all 12 analyses (ns per counted operation)."""
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.2))
    for ax, g in zip(axes.flat, (1, 2, 3, 4)):
        for c in CASES:
            xs = [n for n in SIZES if theo(g, c, n) > 0]
            ys = [t[c][n] / theo(g, c, n) * 1e9 for n in xs]
            if xs:
                ax.loglog(xs, ys, LS[c], marker=MK[c], color=COL[c],
                          label="%s time / %s%d(n)" % (c, {"best": "B", "worst": "W", "average": "A"}[c], g))
        ax.set_title(NAMES[g], fontsize=9.5)
        ax.set_xlabel("input size n")
        ax.set_ylabel("ns per counted operation")
        ax.legend(loc="best", fontsize=7)
    fig.tight_layout()
    save(fig, "time_per_operation.pdf")


def fig_worst_over_avg(t):
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.plot(SIZES, [t["worst"][n] / t["average"][n] for n in SIZES], "none", marker="s",
            color=COL["worst"], label="measured worst / average time")
    ax.plot(NS, [theo(4, "worst", n) / theo(4, "average", n) for n in NS], "-", color=INK2,
            linewidth=1.0, label="W4(n) / A4(n)")
    ax.set_xlabel("input size n")
    ax.set_ylabel("ratio")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, "worst_over_average.pdf")


if __name__ == "__main__":
    times = load_times()
    fig_theory()
    fig_times(times)
    fig_theory_vs_time(times)
    fig_ratio(times)
    fig_worst_over_avg(times)
    print(open(os.path.join(RESULTS, "group4_alpha.csv")).read())
