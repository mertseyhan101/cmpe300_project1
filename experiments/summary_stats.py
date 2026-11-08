"""Numbers quoted in the discussion section -> results/summary.txt"""
import csv, math, os, statistics as st
from common import RESULTS
import formulas as F

rows = list(csv.DictReader(open(os.path.join(RESULTS, "timing.csv"))))
t = {(r["case"], int(r["n"])): float(r["seconds"]) for r in rows if r["case"] in ("best", "worst", "average")}
out = []
def slope(case, n1, n2): return math.log(t[(case, n2)] / t[(case, n1)]) / math.log(n2 / n1)
for c, fn in (("best", F.B4), ("worst", F.W4), ("average", F.AVG[3])):
    out.append("loglog slope %s time 100->400: %.2f   count %s4: %.2f" % (
        c, slope(c, 100, 400), c, math.log(float(fn(400)) / float(fn(100))) / math.log(4)))
inputs = [r for r in rows if r["c4"] and int(r["n"]) >= 40]
for g in (1, 2, 3, 4):
    rat = [float(r["seconds"]) / int(r["c%d" % g]) * 1e9 for r in inputs if int(r["c%d" % g]) > 0]
    out.append("group %d: time/count over %d timed inputs n>=40: min %.1f ns  max %.1f ns  max/min %.1f  CV %.2f"
               % (g, len(rat), min(rat), max(rat), max(rat) / min(rat), st.pstdev(rat) / st.mean(rat)))
runs = {}
for r in rows:
    if r["case"] == "average_run":
        runs.setdefault(int(r["n"]), []).append(float(r["seconds"]))
for n in (100, 400):
    v = runs[n]; out.append("average runs n=%d: min %.3e max %.3e max/min %.2f" % (n, min(v), max(v), max(v) / min(v)))
for n in (100, 200, 400):
    out.append("n=%d worst/average time %.1f   W4/A4 %.1f" % (n, t[("worst", n)] / t[("average", n)], F.W4(n) / float(F.AVG[3](n))))
open(os.path.join(RESULTS, "summary.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
