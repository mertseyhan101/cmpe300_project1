import itertools

import pytest
import reference_interpreter as ref


@pytest.mark.parametrize("d", [2, 3])
def test_all_strings_up_to_length_8(prog, d):
    for n in range(0, 9):
        for tup in itertools.product("abc", repeat=n):
            r, g, _ = ref.run(tup, d)
            res, c = prog.algorithm_counted(list(tup), d)
            assert (res, c) == (r, g), "".join(tup)
            assert prog.algorithm(list(tup), d) == r
