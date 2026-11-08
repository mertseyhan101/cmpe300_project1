from fractions import Fraction


def test_key_and_parameters(prog):
    key, pa, pb, pc, d = prog.variant_of(2023400213, 2023400039)
    assert (2023400213 + 2023400039) % 8 == 4
    assert key == 4
    assert (pa, pb, pc, d) == (Fraction(2, 5), Fraction(2, 5), Fraction(1, 5), 2)
    assert pa + pb + pc == 1


def test_order_of_student_numbers_irrelevant(prog):
    assert prog.variant_of(2023400039, 2023400213) == prog.variant_of(2023400213, 2023400039)


def test_all_variant_rows_sum_to_one(prog):
    for key, (pa, pb, pc, d) in prog.VARIANTS.items():
        assert pa + pb + pc == 1
        assert d == (2 if key % 2 == 0 else 3)


def test_variant_line(prog):
    assert prog.variant_line(*prog.variant_of(2023400213, 2023400039)) == \
        "Variant: 4 (p_a=2/5, p_b=2/5, p_c=1/5, d=2)"
