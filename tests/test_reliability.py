import random
from collections import Counter

import formulas as F


def test_random_input_seeded_reproducible(prog):
    a = prog.random_input(200, F.PA, F.PB, random.Random(42))
    b = prog.random_input(200, F.PA, F.PB, random.Random(42))
    assert a == b and len(a) == 200 and set(a) <= set("abc")


def test_random_input_distribution(prog):
    rng = random.Random(99)
    cnt = Counter(prog.random_input(200000, F.PA, F.PB, rng))
    tot = sum(cnt.values())
    assert abs(cnt["a"] / tot - 0.4) < 0.005
    assert abs(cnt["b"] / tot - 0.4) < 0.005
    assert abs(cnt["c"] / tot - 0.2) < 0.005


def test_algorithm_deterministic(prog):
    rng = random.Random(5)
    for _ in range(50):
        arr = prog.random_input(rng.randint(0, 80), F.PA, F.PB, rng)
        assert prog.algorithm(arr, 2) == prog.algorithm(list(arr), 2) == prog.algorithm_counted(arr, 2)[0]


def test_timing_returns_positive_and_does_not_mutate(prog):
    arr = list("abcab")
    t = prog.time_run(arr, 2)
    assert t > 0 and arr == list("abcab")


def test_experiment_rows(prog, tmp_path):
    import io
    buf = io.StringIO()
    rows = prog.run_experiment(F.PA, F.PB, 2, sizes=[1, 5], runs=10, rng=random.Random(1), out=buf)
    kinds = Counter(r[0] for r in rows)
    assert kinds == {"best": 2, "worst": 2, "average": 2, "average_run": 20}
