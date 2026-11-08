"""Closed-form results of the theoretical analysis (written from the derivations).

General parameters p_a, p_b, p_c (Fractions), d >= 2. lam(n) = floor(log_d n) + 1.
Our variant (key 4): p_a = p_b = 2/5, p_c = 1/5, d = 2.
"""

from fractions import Fraction

PA, PB, PC, D = Fraction(2, 5), Fraction(2, 5), Fraction(1, 5), 2


def lam(n, d=D):
    """floor(log_d n) + 1 computed with integers only (no floating point)."""
    e = 0
    while d ** (e + 1) <= n:
        e += 1
    return e + 1


# ----------------------------- best case ----------------------------------
def B1(n, d=D): return n
def B2(n, d=D): return 0
def B3(n, d=D): return n
def B4(n, d=D):
    L = lam(n, d)
    return n * L - L * (L - 1) // 2


# ----------------------------- worst case ---------------------------------
def W1(n, d=D): return 2 * n
def W2(n, d=D): return n * (n + 1) // 2
def W3(n, d=D): return n + n * n // 4
def W4(n, d=D):
    h, H = n // 2, n - n // 2        # floor(n/2), ceil(n/2)
    return n * (n * n // 4) + n * H + h * lam(n, d)


# ----------------------------- average case -------------------------------
def sum_Es(n, pa=PA, pc=PC):
    """sum_{i=0}^{n-1} E[s_i] = (pa/pc) * (n - (1 - q^n)/pc), q = 1 - pc."""
    q = 1 - pc
    return (pa / pc) * (n - (1 - q ** n) / pc)


def A1(n, pa=PA, pb=PB, pc=PC, d=D):
    return (2 - pa) * n


def A2(n, pa=PA, pb=PB, pc=PC, d=D):
    return pb * (n + sum_Es(n, pa, pc)) + pc * Fraction(n * (n + 1), 2)


def A3(n, pa=PA, pb=PB, pc=PC, d=D):
    return (pa + pc) * n + pb * (n + sum_Es(n, pa, pc))


def A4(n, pa=PA, pb=PB, pc=PC, d=D):
    return pa * n * lam(n, d) + pb * n * (n + sum_Es(n, pa, pc)) + pc * Fraction(n * (n + 1), 2)


# ------------- variant-specific simplified closed forms (key 4) -----------
def A1_v(n): return Fraction(8, 5) * n
def A2_v(n): return Fraction(n * n, 10) + Fraction(13, 10) * n - 4 + 4 * Fraction(4, 5) ** n
def A3_v(n): return Fraction(9, 5) * n - 4 + 4 * Fraction(4, 5) ** n
def A4_v(n):
    return (Fraction(13, 10) * n * n - Fraction(39, 10) * n
            + Fraction(2, 5) * n * lam(n) + 4 * n * Fraction(4, 5) ** n)


BEST = [B1, B2, B3, B4]
WORST = [W1, W2, W3, W4]
AVG = [A1_v, A2_v, A3_v, A4_v]
AVG_GENERAL = [A1, A2, A3, A4]


# --------------------- best / worst inputs per group ----------------------
def best_input(g, n, d=D):
    if g == 4:
        L = lam(n, d)
        return "a" * (n - L) + "c" * L
    return "a" * n                       # groups 1, 2, 3


def worst_input(g, n, d=D):
    if g == 1:
        return "b" * n                   # any string without 'a'
    if g == 2:
        return "c" * n
    return "a" * (n // 2) + "b" * (n - n // 2)   # groups 3 and 4
