"""Independent verification of the 12 closed forms.

1. Exhaustive: all 3^n strings, n = 1..10, run through the reference interpreter;
   min / max per group compared with B(n), W(n); stated inputs checked;
   exact expectation (Fraction weights) compared with A(n) for n = 1..9.
2. DP: exact min / max over all 3^n strings via dynamic programming over (i, s),
   n = 1..120 (does not use the proofs, only the per-character cost model, which
   itself is checked against the interpreter on random long strings).
3. Exact expectation via the distribution of s (Fractions), n up to 150.
4. sympy: symbolic derivation of A1..A4 from the expectation sums and
   comparison with the simplified variant formulas; asymptotic limits.
Writes a log to results/math_verification.txt and exits non-zero on any failure.
"""

import itertools
import os
import random
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tests"))
sys.path.insert(0, os.path.join(ROOT, "analysis"))

import reference_interpreter as ref  # noqa: E402
import formulas as F                  # noqa: E402

P = {"a": F.PA, "b": F.PB, "c": F.PC}
log_lines = []
failures = []


def log(msg):
    print(msg)
    log_lines.append(msg)


def check(cond, msg):
    if not cond:
        failures.append(msg)
        log("FAIL: " + msg)


# ---------------------------------------------------------------- 1. exhaustive
def exhaustive(nmax=10, emax=9):
    log("== 1. Exhaustive enumeration (reference interpreter) ==")
    for n in range(1, nmax + 1):
        mins = [None] * 4
        maxs = [None] * 4
        exp = [Fraction(0)] * 4
        for tup in itertools.product("abc", repeat=n):
            _, g, _ = ref.run(tup, F.D)
            if n <= emax:
                w = Fraction(1)
                for ch in tup:
                    w *= P[ch]
                for j in range(4):
                    exp[j] += w * g[j]
            for j in range(4):
                mins[j] = g[j] if mins[j] is None else min(mins[j], g[j])
                maxs[j] = g[j] if maxs[j] is None else max(maxs[j], g[j])
        for j in range(4):
            gnum = j + 1
            check(mins[j] == F.BEST[j](n), "B%d(%d): exhaustive %s formula %s" % (gnum, n, mins[j], F.BEST[j](n)))
            check(maxs[j] == F.WORST[j](n), "W%d(%d): exhaustive %s formula %s" % (gnum, n, maxs[j], F.WORST[j](n)))
            bi, wi = F.best_input(gnum, n), F.worst_input(gnum, n)
            check(len(bi) == n and len(wi) == n, "input length")
            check(ref.run(bi, F.D)[1][j] == F.BEST[j](n), "best input group %d n=%d" % (gnum, n))
            check(ref.run(wi, F.D)[1][j] == F.WORST[j](n), "worst input group %d n=%d" % (gnum, n))
            if n <= emax:
                check(exp[j] == F.AVG[j](n), "A%d(%d): exact %s formula %s" % (gnum, n, exp[j], F.AVG[j](n)))
                check(exp[j] == F.AVG_GENERAL[j](n), "A%d general (%d)" % (gnum, n))
        log("n=%2d  min=%s  max=%s%s" % (n, mins, maxs,
            ("  E=" + str([str(x) for x in exp])) if n <= emax else ""))


# ---------------------------------------------------------- per-character costs
def cost(g, ch, i, s, n, d=F.D):
    """Cost of one outer iteration for group g (derived in the report, Section 4)."""
    L = F.lam(n, d)
    if g == 1:
        return 1 if ch == "a" else 2
    if g == 2:
        return {"a": 0, "b": s + 1, "c": n - i}[ch]
    if g == 3:
        return {"a": 1, "b": s + 1, "c": 1}[ch]
    return {"a": L, "b": n * (s + 1), "c": n - i}[ch]


def next_s(ch, s):
    return s + 1 if ch == "a" else (s if ch == "b" else 0)


def cost_model_vs_interpreter(trials=300):
    log("== 2a. Per-character cost model vs interpreter on random strings (n up to 60) ==")
    rng = random.Random(12345)
    for _ in range(trials):
        n = rng.randint(1, 60)
        text = "".join(rng.choice("abc") for _ in range(n))
        _, g, _ = ref.run(text, F.D)
        s = 0
        tot = [0, 0, 0, 0]
        for i, ch in enumerate(text):
            for j in range(4):
                tot[j] += cost(j + 1, ch, i, s, n)
            s = next_s(ch, s)
        check(tot == g, "cost model mismatch on %s" % text)
    log("checked %d random strings" % trials)


def dp_opt(g, n, best):
    """Exact min (best=True) or max over all strings of length n."""
    agg = min if best else max
    # V[s] = optimal cost of positions i..n-1 given current s
    V = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        newV = [0] * (i + 1)
        for s in range(i + 1):
            newV[s] = agg(cost(g, ch, i, s, n) + V[next_s(ch, s)] for ch in "abc")
        V = newV
    return V[0]


def dp_check(nmax=120):
    log("== 2b. DP optimum over all 3^n strings, n = 1..%d ==" % nmax)
    for n in range(1, nmax + 1):
        for j in range(4):
            b, w = dp_opt(j + 1, n, True), dp_opt(j + 1, n, False)
            check(b == F.BEST[j](n), "DP B%d(%d)=%d formula %d" % (j + 1, n, b, F.BEST[j](n)))
            check(w == F.WORST[j](n), "DP W%d(%d)=%d formula %d" % (j + 1, n, w, F.WORST[j](n)))
    log("all B/W formulas equal the DP optimum for n = 1..%d" % nmax)


# ------------------------------------------------ 3. exact expectation via s-distribution
def exact_expectation(n):
    dist = {0: Fraction(1)}   # distribution of s before position i
    E = [Fraction(0)] * 4
    for i in range(n):
        nd = {}
        for s, ps in dist.items():
            for ch in "abc":
                w = ps * P[ch]
                for j in range(4):
                    E[j] += w * cost(j + 1, ch, i, s, n)
                s2 = next_s(ch, s)
                nd[s2] = nd.get(s2, 0) + w
        dist = nd
    return E


def expectation_check():
    log("== 3. Exact expectation via distribution of s ==")
    for n in list(range(1, 41)) + [50, 60, 80, 100, 150]:
        E = exact_expectation(n)
        for j in range(4):
            check(E[j] == F.AVG[j](n), "A%d(%d) dist=%s formula=%s" % (j + 1, n, E[j], F.AVG[j](n)))
    log("A1..A4 equal the exact expectation for n = 1..40, 50, 60, 80, 100, 150")


# ------------------------------------------------------------------ 4. sympy
def sympy_check():
    import sympy as sp
    log("== 4. sympy symbolic checks ==")
    n, i, j = sp.symbols("n i j", integer=True, nonnegative=True)
    pa, pb, pc = sp.symbols("p_a p_b p_c", positive=True)
    q = 1 - pc
    # E[s_i] from the indicator sum sum_{j=0}^{i-1} pa q^(i-1-j)
    Es_ind = sp.simplify(sp.summation(pa * q ** (i - 1 - j), (j, 0, i - 1)))
    Es_closed = pa / pc * (1 - q ** i)
    log("E[s_i] indicator sum == closed form: %s" % sp.simplify(Es_ind - Es_closed).equals(0))
    check(sp.simplify(Es_ind - Es_closed) == 0 or sp.simplify(Es_ind - Es_closed).equals(0), "E[s_i]")
    # recurrence E[s_{i+1}] = q E[s_i] + pa
    rec = sp.simplify(Es_closed.subs(i, i + 1) - (q * Es_closed + pa))
    check(rec == 0, "E[s] recurrence")
    log("E[s_i] satisfies E[s_{i+1}] = (1-p_c)E[s_i] + p_a, E[s_0]=0: %s" % (rec == 0 and Es_closed.subs(i, 0) == 0))
    S = sp.simplify(sp.summation(Es_closed, (i, 0, n - 1)))
    lam = sp.Symbol("lambda", positive=True)
    gen = {
        1: sp.summation(pa * 1 + (pb + pc) * 2, (i, 0, n - 1)),
        2: sp.summation(pb * (Es_closed + 1) + pc * (n - i), (i, 0, n - 1)),
        3: sp.summation(pa + pb * (Es_closed + 1) + pc, (i, 0, n - 1)),
        4: sp.summation(pa * lam + pb * n * (Es_closed + 1) + pc * (n - i), (i, 0, n - 1)),
    }
    sub = {pa: sp.Rational(2, 5), pb: sp.Rational(2, 5), pc: sp.Rational(1, 5)}
    r45 = sp.Rational(4, 5)
    variant = {
        1: sp.Rational(8, 5) * n,
        2: n ** 2 / 10 + sp.Rational(13, 10) * n - 4 + 4 * r45 ** n,
        3: sp.Rational(9, 5) * n - 4 + 4 * r45 ** n,
        4: sp.Rational(13, 10) * n ** 2 - sp.Rational(39, 10) * n + sp.Rational(2, 5) * n * lam + 4 * n * r45 ** n,
    }
    for g in (1, 2, 3, 4):
        diff = sp.simplify(sp.expand(gen[g].subs(sub) - variant[g]))
        ok = diff == 0 or all(sp.simplify(diff.subs(n, v).subs(lam, 3)) == 0 for v in range(1, 30))
        check(ok, "sympy A%d" % g)
        log("A%d(n) general = %s ;  variant simplified matches: %s" % (g, sp.simplify(gen[g]), ok))
    # asymptotic ratios
    x = sp.Symbol("x", positive=True)
    lims = {
        "A1/n": sp.limit(variant[1] / n, n, sp.oo),
        "A2/n^2": sp.limit(variant[2] / n ** 2, n, sp.oo),
        "A3/n": sp.limit(variant[3] / n, n, sp.oo),
        "A4/n^2 (lambda~log2 n)": sp.limit(variant[4].subs(lam, sp.log(n, 2) + 1) / n ** 2, n, sp.oo),
        "W4/n^3 (n even)": sp.limit((n * n ** 2 / 4 + n * n / 2 + n / 2 * (sp.log(n, 2) + 1)) / n ** 3, n, sp.oo),
        "B4/(n log2 n)": sp.limit((n * (sp.log(n, 2) + 1) - (sp.log(n, 2) + 1) * sp.log(n, 2) / 2) / (n * sp.log(n, 2)), n, sp.oo),
    }
    for k, v in lims.items():
        log("limit %s = %s" % (k, v))
    check(lims["A1/n"] == sp.Rational(8, 5) and lims["A2/n^2"] == sp.Rational(1, 10), "limits")
    check(lims["A4/n^2 (lambda~log2 n)"] == sp.Rational(13, 10) and lims["W4/n^3 (n even)"] == sp.Rational(1, 4), "limits 4")
    check(lims["B4/(n log2 n)"] == 1, "limit B4")


if __name__ == "__main__":
    exhaustive()
    cost_model_vs_interpreter()
    dp_check()
    expectation_check()
    sympy_check()
    log("")
    log("FAILURES: %d" % len(failures))
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "math_verification.txt"), "w") as fh:
        fh.write("\n".join(log_lines) + "\n")
    sys.exit(1 if failures else 0)
