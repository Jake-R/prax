from hypothesis import given, example, settings, strategies as st, HealthCheck

from prax import *


@given(st.text(), st.text())
def test_add(x, y):
    assert (p(x) + p(y)).utf_8 == x + y


@given(st.text(), st.integers().filter(lambda x: 0 <= x <= 100))
def test_multiply(x, y):
    assert (p(x) * y).utf_8 == x * y


@given(st.binary(), st.binary())
def test_eq(x, y):
    assert (p(x) == p(y)) == (x == y)


@given(st.binary(), st.binary())
def test_neq(x, y):
    assert (p(x) != p(y)) == (x != y)


def perms(x, y, func):
    assert func(p(x), y).num == func(x, y)
    assert func(p(x), p(y)).num == func(x, y)
    assert func(p(x), p(y)).num == func(x, y)


@given(st.integers().filter(lambda x: 0 <= x), st.integers().filter(lambda x: 0 <= x <= 100))
@settings(suppress_health_check=[HealthCheck.filter_too_much])
def test_lshift(x, y):
    perms(x, y, lambda x, y: x << y)


@given(st.integers().filter(lambda x: 0 <= x), st.integers().filter(lambda x: 0 <= x <= 100))
@settings(suppress_health_check=[HealthCheck.filter_too_much])
def test_rshift(x, y):
    perms(x, y, lambda x, y: x >> y)

@given(st.integers().filter(lambda x: 0 <= x), st.integers().filter(lambda x: 0 <= x <= 100))
@settings(suppress_health_check=[HealthCheck.filter_too_much])
def test_increment(x, y):
    # TODO: implement
    assert True

@given(st.integers().filter(lambda x: 0 <= x), st.integers().filter(lambda x: 0 <= x))
def test_and(x, y):
    perms(x, y, lambda x, y: x & y)


@given(st.integers().filter(lambda x: 0 <= x), st.integers().filter(lambda x: 0 <= x))
def test_xor(x, y):
    perms(x, y, lambda x, y: x ^ y)


@given(st.integers().filter(lambda x: 0 <= x), st.integers().filter(lambda x: 0 <= x))
def test_or(x, y):
    perms(x, y, lambda x, y: x | y)
