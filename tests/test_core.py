from hypothesis import given, example, strategies as st

from prax import *


@given(st.text())
def test_utf_8(s):
    assert p(s).utf_8 == s


@given(st.binary())
@example(b"")
def test_raw(s):
    assert p(s).raw == s.decode('latin-1')


@given(st.integers().filter(lambda x: x >= 0))
def test_num(i):
    assert p(i).num == i


@given(st.binary())
def test_endian_swap(b):
    assert p(b).e(len(b)).e(len(b)).bytes == b


@given(st.binary().filter(lambda x: len(x) % 4 == 0))
def test_endian_swap2(b):
    assert p(b).e().e().bytes == b
