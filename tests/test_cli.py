import re
import subprocess
import sys

import formulas as F
import pytest
import reference_interpreter as ref
from conftest import PROGRAM

VARIANT = "Variant: 4 (p_a=2/5, p_b=2/5, p_c=1/5, d=2)"


def run(*args, timeout=120):
    return subprocess.run([sys.executable, PROGRAM, *args], capture_output=True, text=True, timeout=timeout)


@pytest.mark.parametrize("text", ["aabcbba", "abcabcba", "a", "b", "c", "cccccc", "aaaabbbb",
                                  "bacbacbacbacbacbacba", "a" * 50 + "b" * 50])
def test_count_mode_exact_output(text):
    p = run("2023400213", "2023400039", "--count", text)
    assert p.returncode == 0
    assert p.stderr == ""
    _, g, _ = ref.run(text, 2)
    assert p.stdout == VARIANT + "\n" + "Count(1): {} Count(2): {} Count(3): {} Count(4): {}\n".format(*g)


def test_count_mode_order_of_numbers():
    p = run("2023400039", "2023400213", "--count", "abc")
    assert p.stdout.splitlines()[0] == VARIANT


def test_count_mode_other_variant_uses_its_d():
    # 1 + 4 = 5 -> key 5, d = 3
    p = run("1", "4", "--count", "aaaaaaaaa")
    lines = p.stdout.splitlines()
    assert lines[0] == "Variant: 5 (p_a=2/5, p_b=2/5, p_c=1/5, d=3)"
    assert lines[1] == "Count(1): 9 Count(2): 0 Count(3): 9 Count(4): 27"


def test_count_mode_large_hidden_like_input():
    text = ("aab" * 40 + "c" + "ba" * 30)[:200]
    p = run("2023400213", "2023400039", "--count", text)
    _, g, _ = ref.run(text, 2)
    assert p.stdout.splitlines()[1] == "Count(1): {} Count(2): {} Count(3): {} Count(4): {}".format(*g)


def test_count_mode_empty_string():
    p = run("2023400213", "2023400039", "--count", "")
    assert p.returncode == 0
    assert p.stdout.splitlines() == [VARIANT, "Count(1): 0 Count(2): 0 Count(3): 0 Count(4): 0"]


@pytest.mark.parametrize("args", [[], ["2023400213"], ["x", "y"], ["1", "2", "--cnt", "abc"],
                                  ["1", "2", "--count", "abd"], ["1", "2", "--count"]])
def test_bad_arguments(args):
    p = run(*args)
    assert p.returncode != 0
    assert p.stdout == ""
    assert p.stderr != ""


def test_normal_mode_format():
    p = run("2023400213", "2023400039", timeout=600)
    assert p.returncode == 0 and p.stderr == ""
    lines = p.stdout.splitlines()
    assert lines[0] == VARIANT
    case_re = re.compile(r"^Case: (best|worst|average) Size: (\d+) Elapsed Time \(s\): (\d+\.\d+)$")
    cases = [case_re.match(l) for l in lines[1:] if l.startswith("Case:")]
    assert all(cases)
    got = [(m.group(1), int(m.group(2))) for m in cases]
    sizes = [1, 5, 10, 20, 40, 50, 60, 80, 100, 150, 200, 250, 300, 350, 400]
    assert got == [(c, n) for c in ("best", "worst", "average") for n in sizes]
    runs = [l for l in lines if l.startswith("    Runs (s): ")]
    assert len(runs) == 15
    for l in runs:
        vals = l.split(": ", 1)[1].split(", ")
        assert len(vals) == 10 and all(float(v) > 0 for v in vals)
    # every line is either the variant, a Case line or a Runs line
    assert len(lines) == 1 + 45 + 15
