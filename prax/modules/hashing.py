import hashlib
import zlib

from prax import *


@praxfunction
@praxmethod
def crc32(pb):
    """crc32 of input"""
    pb = p(pb)
    n = zlib.crc32(pb.bytes)
    # zlib returns crc32 as 32 bit signed integer. we don't care about sign
    return p(n if n >= 0 else n + (1 << 32))


@praxfunction
@praxmethod
def md5(pb):
    """md5 sum of input"""
    pb = p(pb)
    return p(hashlib.md5(pb.bytes).digest())


@praxfunction
@praxmethod
def sha1(pb):
    """sha1 sum of input"""
    pb = p(pb)
    return p(hashlib.sha1(pb.bytes).digest())


@praxfunction
@praxmethod
def sha256(pb):
    """sha256 sum of input"""
    pb = p(pb)
    return p(hashlib.sha256(pb.bytes).digest())


@praxfunction
@praxmethod
def sha512(pb):
    """sha512 sum of input"""
    pb = p(pb)
    return p(hashlib.sha512(pb.bytes).digest())




