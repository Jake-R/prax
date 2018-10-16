import hashlib
import zlib
from prax import *

from hypothesis import given, example, strategies as st


@given(st.binary())
@example(b"")
def test_crc32(s):
    n = zlib.crc32(s)
    assert crc32(s).num == n if n >= 0 else n + (1 << 32)


@given(st.binary())
@example(b"")
def test_md5(s):
    assert md5(s) == hashlib.md5(s).digest()


@given(st.binary())
@example(b"")
def test_sha1(s):
    assert sha1(s) == hashlib.sha1(s).digest()


@given(st.binary())
@example(b"")
def test_sha256(s):
    assert sha256(s) == hashlib.sha256(s).digest()


@given(st.binary())
@example(b"")
def test_sha512(s):
    assert sha512(s) == hashlib.sha512(s).digest()
