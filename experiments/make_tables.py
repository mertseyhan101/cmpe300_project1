"""Fill the four official tables (layout of report_tables.tex kept) from results/*.csv."""
import csv
import os

from common import RESULTS, ROOT

OUT = os.path.join(ROOT, "report", "generated")
os.makedirs(OUT, exist_ok=True)

LOG = r"\lfloor \log_2 n\rfloor"
T1 = {
    1: [("n", r"\Theta(n)"), ("2n", r"\Theta(n)"), (r"\frac{8n}{5}", r"\Theta(n)")],
    2: [("0", r"O(1)\ (\text{constant } 0)"), (r"\frac{n(n+1)}{2}", r"\Theta(n^2)"),
        (r"\frac{n^2}{10}+\frac{13n}{10}-4+4\left(\frac{4}{5}\right)^{n}", r"\Theta(n^2)")],
    3: [("n", r"\Theta(n)"), (r"n+\left\lfloor \frac{n^2}{4}\right\rfloor", r"\Theta(n^2)"),
        (r"\frac{9n}{5}-4+4\left(\frac{4}{5}\right)^{n}", r"\Theta(n)")],
    4: [(r"n\lambda-\frac{\lambda(\lambda-1)}{2},\ \ \lambda=" + LOG + "+1", r"\Theta(n\log n)"),
        (r"n\left\lfloor \frac{n^2}{4}\right\rfloor+n\left\lceil \frac{n}{2}\right\rceil+\left\lfloor \frac{n}{2}\right\rfloor\left(" + LOG + r"+1\right)", r"\Theta(n^3)"),
        (r"\frac{13n^2}{10}-\frac{39n}{10}+\frac{2n}{5}\left(" + LOG + r"+1\right)+4n\left(\frac{4}{5}\right)^{n}", r"\Theta(n^2)")],
}
GROUP_CELL = {1: "(1)\\\\comparisons", 2: "(2)\\\\loop increments", 3: "(3)\\\\assignments", 4: "(4)\\\\assignments"}


def variant_table():
    return r"""\begin{center}
\begin{tabular}{|C{2.2cm}|C{2.2cm}|C{2.2cm}|C{2.2cm}|C{2.2cm}|}
\hline
\textbf{key} & $\boldsymbol{p_a}$ & $\boldsymbol{p_b}$ & $\boldsymbol{p_c}$ & $\boldsymbol{d}$ \\ \hline
\fillcell 4 & $2/5$ & $2/5$ & $1/5$ & $2$ \\ \hline
\end{tabular}
\end{center}
"""


def table1():
    L = [r"\begin{longtable}{|C{2.3cm}|C{1.5cm}|p{7.2cm}|C{3.0cm}|}",
         r"\hline",
         r"\textbf{Basic operation} & \textbf{Case} & \centering\arraybackslash\textbf{Exact count (closed form)} & \textbf{Asymptotic} \\ \hline",
         r"\endhead", r"\hline", r"\endfoot"]
    for g in (1, 2, 3, 4):
        L.append("%% --- Case %d ---" % g)
        for k, (case, (exact, asym)) in enumerate(zip("BWA", T1[g])):
            first = (r"\multirow{3}{*}{\parbox{2.3cm}{\centering %s}}" % GROUP_CELL[g]) if k == 0 else ""
            end = r" \\ \hline" if k == 2 else r" \\ \cline{2-4}"
            L.append(r"%s & $%s_%d(n)$ & \fillcell $\displaystyle %s$ & $%s$%s" % (first, case, g, exact, asym, end))
    L.append(r"\end{longtable}")
    return "\n".join(L) + "\n"


def fmt_time(x):
    return "%.6e" % x


def table2():
    t = {}
    for r in csv.DictReader(open(os.path.join(RESULTS, "timing.csv"))):
        if r["case"] in ("best", "worst", "average"):
            t[(r["case"], int(r["n"]))] = float(r["seconds"])
    info = dict(l.strip().split(": ", 1) for l in open(os.path.join(RESULTS, "machine.txt")) if ": " in l)
    mem = int(info["memory_bytes"]) // 2 ** 30
    L = [r"Basic operation identified as the ``correct'' one: \underline{group (4): assignments on lines 7, 12, 16}\\[0.4em]",
         r"Programming language / machine: \underline{%s / MacBook Air, %s, %d GB, macOS 15.5}" % (
             info["python"].replace("CPython", "Python"), info["cpu"], mem),
         "", r"\begin{center}", r"\begin{tabular}{|C{1.6cm}|C{3.4cm}|C{3.4cm}|C{3.8cm}|}", r"\hline",
         r"$n$ & \textbf{Best (s)} & \textbf{Worst (s)} & \textbf{Average (s)} \\ \hline"]
    for n in [1, 5, 10, 20, 40, 50, 60, 80, 100, 150, 200, 250, 300, 350, 400]:
        L.append(r"%-3d & \fillcell %s & %s & %s \\ \hline" % (n, fmt_time(t[("best", n)]), fmt_time(t[("worst", n)]), fmt_time(t[("average", n)])))
    L += [r"\end{tabular}", r"\end{center}"]
    return "\n".join(L) + "\n"


def table3():
    rows = list(csv.DictReader(open(os.path.join(RESULTS, "table3.csv"))))
    L = [r"\begin{longtable}{|C{2.3cm}|C{1.2cm}|C{2.6cm}|C{2.6cm}|C{2.6cm}|C{2.6cm}|}", r"\hline",
         r"\textbf{Basic operation} & $\boldsymbol{n}$ & \textbf{Counted best} & \textbf{Formula $B(n)$} & \textbf{Counted worst} & \textbf{Formula $W(n)$} \\ \hline",
         r"\endhead", r"\hline", r"\endfoot"]
    for g in (1, 2, 3, 4):
        grp = [r for r in rows if int(r["group"]) == g]
        for k, r in enumerate(grp):
            first = (r"\multirow{6}{*}{\parbox{2.3cm}{\centering %s}}" % GROUP_CELL[g]) if k == 0 else ""
            end = r" \\ \hline" if k == len(grp) - 1 else r" \\ \cline{2-6}"
            L.append(r"%s & %s & \fillrow %s & %s & %s & %s%s" % (first, r["n"], r["counted_best"], r["formula_B"],
                                                                 r["counted_worst"], r["formula_W"], end))
    L.append(r"\end{longtable}")
    return "\n".join(L) + "\n"


def table4():
    rows = list(csv.DictReader(open(os.path.join(RESULTS, "table4.csv"))))
    N = rows[0]["N"]
    L = [r"\noindent Number of random inputs used for each $n$ ($N\ge 1000$): \underline{\hspace{1cm}%s\hspace{1cm}}" % N, "",
         r"\begin{center}", r"\begin{longtable}{|C{2.3cm}|C{1.2cm}|C{3.4cm}|C{3.0cm}|C{2.8cm}|}", r"\hline",
         r"\textbf{Basic operation} & $\boldsymbol{n}$ & \textbf{Mean of counted values} & \textbf{Formula $A(n)$} & \textbf{Difference} \\ \hline",
         r"\endhead", r"\hline", r"\endfoot"]
    for g in (1, 2, 3, 4):
        grp = [r for r in rows if int(r["group"]) == g]
        for k, r in enumerate(grp):
            first = (r"\multirow{3}{*}{\parbox{2.3cm}{\centering %s}}" % GROUP_CELL[g]) if k == 0 else ""
            end = r" \\ \hline" if k == len(grp) - 1 else r" \\ \cline{2-5}"
            L.append(r"%s & %s & \fillrow %.3f & %.4f & %+.3f%s" % (
                first, r["n"], float(r["mean"]), float(r["A_float"]), float(r["diff"]), end))
    L += [r"\end{longtable}", r"\end{center}"]
    return "\n".join(L) + "\n"


def table4_stats():
    """Supplementary table: standard errors (not part of the official template)."""
    rows = list(csv.DictReader(open(os.path.join(RESULTS, "table4.csv"))))
    L = [r"\begin{tabular}{cccccc}", r"\toprule",
         r"group & $n$ & difference & relative difference & std.\ error $\hat\sigma/\sqrt N$ & difference / std.\ error \\ \midrule"]
    for r in rows:
        d, se = float(r["diff"]), float(r["std_error"])
        L.append(r"(%s) & %s & %+.3f & %+.2f\%% & %.3f & %+.2f \\" % (r["group"], r["n"], d, 100 * float(r["rel_diff"]), se, d / se if se else 0.0))
    L += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(L) + "\n"


def extremes():
    rows = list(csv.DictReader(open(os.path.join(RESULTS, "extremes_timing.csv"))))
    rows = [r for r in rows if r["n"] == "400"]
    L = [r"\begin{tabular}{cllrrrrr}", r"\toprule",
         r"group & case & input & time (s) & $c_1$ & $c_2$ & $c_3$ & $c_4$ \\ \midrule"]
    for r in rows:
        inp = r["input_desc"].replace("^(n-L)", "^{n-\\lambda}").replace("c^L", "c^{\\lambda}").replace("^(n/2)", "^{n/2}").replace("^n", "^{n}")
        L.append(r"(%s) & %s & $%s$ & %.2e & %s & %s & %s & %s \\" % (r["group"], r["kind"], inp, float(r["seconds"]),
                                                                    r["c1"], r["c2"], r["c3"], r["c4"]))
    L += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    for name, fn in [("variant", variant_table), ("table1", table1), ("table2", table2), ("table3", table3),
                     ("table4", table4), ("table4_stats", table4_stats), ("extremes", extremes)]:
        with open(os.path.join(OUT, name + ".tex"), "w") as fh:
            fh.write(fn())
    print("tables written to", OUT)
