import pytest
import reference_interpreter as ref

D = 2


def counts(prog, text, d=D):
    return prog.algorithm_counted(list(text), d)


def test_hand_computed_example(prog):
    # computed by hand in the report: n=8, lambda=4
    res, c = counts(prog, "abcabcba")
    assert res == 227
    assert c == [13, 14, 10, 61]
    assert prog.algorithm(list("abcabcba"), D) == 227


@pytest.mark.parametrize("text,expected", [
    ("a", (0, [1, 0, 1, 1])),     # k: 1 -> 0, one iteration of line 7
    ("b", (1, [2, 1, 1, 1])),     # q = 0 only; r = 1 only: res = 0 + 1
    ("c", (0, [2, 1, 1, 1])),     # t = 0 only
])
def test_single_characters(prog, text, expected):
    assert counts(prog, text) == expected


def test_while_loop_floor_division(prog):
    # k = n, n//2, ... ; iterations = floor(log2 n) + 1
    for n, it in [(1, 1), (2, 2), (3, 2), (4, 3), (7, 3), (8, 4), (100, 7), (400, 9)]:
        assert counts(prog, "a" * n)[1][3] == n * it
        assert prog.log_steps(n, 2) == it
    assert prog.log_steps(9, 3) == 3 and prog.log_steps(8, 3) == 2


def test_s_persists_across_b(prog):
    # a b a b : second b sees s = 2 (b does not reset s)
    _, c = counts(prog, "abab")
    assert c[1] == 2 + 3
    assert c[2] == 1 + 2 + 1 + 3


def test_s_reset_by_c(prog):
    _, c = counts(prog, "aacb")
    # c at i=2: 2 increments; b sees s = 0: 1 increment
    assert c[1] == 2 + 1


def test_s_not_reset_per_iteration(prog):
    # the b at the end sees all preceding a's
    _, c = counts(prog, "aaaab")
    assert c[1] == 5 and c[3] == 4 * 3 + 5 * 5


def test_c_loop_depends_on_position(prog):
    for n in range(1, 12):
        _, c = counts(prog, "c" * n)
        assert c[1] == n * (n + 1) // 2 == c[3]


def test_result_value_branches(prog):
    # b with s=1, n=3: q=0,1 -> res += 0+1, plus 2*(1+2+3)
    assert prog.algorithm(list("ab" + "c"), D) == ref.run("abc", D)[0]
    assert prog.algorithm(list("ab"), D) == 1 + 2 * 3


def test_empty_input(prog):
    assert counts(prog, "") == (0, [0, 0, 0, 0])


def test_matches_reference_on_mixed_inputs(prog):
    for text in ["aaabbbccc", "cbacba", "bbbb", "aaaa", "cccc", "abcabcabcabc", "bacbacab"]:
        r, g, _ = ref.run(text, D)
        assert counts(prog, text) == (r, g)
        assert prog.algorithm(list(text), D) == r
