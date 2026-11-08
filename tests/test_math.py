import itertools
import random
from fractions import Fraction

import formulas as F
import pytest

P = {"a": F.PA, "b": F.PB, "c": F.PC}


@pytest.mark.parametrize("n", range(1, 9))
def test_best_worst_exhaustive(prog, n):
    allc = [prog.algorithm_counted(list(t), 2)[1] for t in itertools.product("abc", repeat=n)]
    for g in range(4):
        vals = [c[g] for c in allc]
        assert min(vals) == F.BEST[g](n)
        assert max(vals) == F.WORST[g](n)


@pytest.mark.parametrize("n", [1, 2, 3, 5, 10, 20, 40, 100, 150, 400])
def test_stated_inputs_attain_formulas(prog, n):
    for g in range(4):
        b = prog.algorithm_counted(list(F.best_input(g + 1, n)), 2)[1][g]
        w = prog.algorithm_counted(list(F.worst_input(g + 1, n)), 2)[1][g]
        assert b == F.BEST[g](n)
        assert w == F.WORST[g](n)


def test_program_generators_are_group4_extremes(prog):
    for n in [1, 5, 10, 40, 100, 400]:
        assert "".join(prog.best_input(n, 2)) == F.best_input(4, n)
        assert "".join(prog.worst_input(n, 2)) == F.worst_input(4, n)


@pytest.mark.parametrize("n", range(1, 8))
def test_average_exact_enumeration(prog, n):
    E = [Fraction(0)] * 4
    for t in itertools.product("abc", repeat=n):
        w = Fraction(1)
        for ch in t:
            w *= P[ch]
        c = prog.algorithm_counted(list(t), 2)[1]
        for g in range(4):
            E[g] += w * c[g]
    for g in range(4):
        assert E[g] == F.AVG[g](n) == F.AVG_GENERAL[g](n)


def test_formulas_special_values():
    assert [f(1) for f in F.BEST] == [1, 0, 1, 1]
    assert [f(1) for f in F.WORST] == [2, 1, 1, 1]
    assert [F.AVG[g](1) for g in range(4)] == [Fraction(8, 5), Fraction(3, 5), 1, 1]
    assert F.lam(1) == 1 and F.lam(2) == 2 and F.lam(1023) == 10 and F.lam(1024) == 11


def test_random_inputs_between_best_and_worst(prog):
    rng = random.Random(2023)
    for _ in range(500):
        n = rng.randint(1, 60)
        c = prog.algorithm_counted(prog.random_input(n, F.PA, F.PB, rng), 2)[1]
        for g in range(4):
            assert F.BEST[g](n) <= c[g] <= F.WORST[g](n)


def test_monte_carlo_close_to_average(prog):
    rng = random.Random(7)
    n, N = 40, 3000
    sums = [0, 0, 0, 0]
    for _ in range(N):
        c = prog.algorithm_counted(prog.random_input(n, F.PA, F.PB, rng), 2)[1]
        for g in range(4):
            sums[g] += c[g]
    for g in range(4):
        mean = sums[g] / N
        assert abs(mean - float(F.AVG[g](n))) / float(F.AVG[g](n)) < 0.03
