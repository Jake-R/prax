from __future__ import absolute_import, division, print_function
from builtins import *

import math
import binascii
import types
import sys


funcs = []


def praxfunction(func):
    funcs.append(func)
    return func


def isiterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def int_from_bytes(bytes_, endianness='big'):
    return int.from_bytes(bytes_, endianness)


def int_to_bytes(int_, endianness='big'):
    """Helper to convert int to properly sized bytes object"""
    return int_.to_bytes((int_.bit_length() + 7) // 8, endianness)


def pad_even(input_, padding='0'):
    if len(input_) % 2 != 0:
        return b'0' + input_
    return input_


class PraxException(BaseException):
    pass


class PraxBytes(object):
    def __init__(self, input):
        if isinstance(input, PraxBytes):
            self.bytes = input.bytes
        elif isinstance(input, str):

            self.bytes = bytes(input, encoding='utf-8')
        elif isiterable(input):
            self.bytes = bytes(input)
        elif isinstance(input, int):
            self.bytes = int_to_bytes(int(input), 'big')
        else:
            raise PraxException("Cannot create PB object with input type {}".format(type(input)))
        for item in funcs:
            setattr(self, item.__name__, types.MethodType(item, self))

    def __str__(self):
        return self.bytes

    def __repr__(self):
        raw = self.H().raw
        if len(raw) > 50:
            raw = "{}...".format(raw[:50])
        return "<PraxBytes: 0x{}>".format(raw)

    def __eq__(self, other):
        try:
            return self.bytes == PraxBytes(other).bytes
        except PraxException:
            return NotImplemented

    @staticmethod
    def _realadd(left, right):
        try:
            return PraxBytes(PraxBytes(left).bytes + PraxBytes(right).bytes)
        except PraxException:
            return NotImplemented

    def __add__(self, other):
        return self._realadd(self, other)

    def __radd__(self, other):
        return self._realadd(other, self)

    def __getitem__(self, item):
        return PraxBytes(self.bytes.__getitem__(item))

    def __contains__(self, item):
        return self.bytes.__contains__(PraxBytes(item).bytes)


p = PraxBytes


def praxoutput(func):
    setattr(PraxBytes, func.__name__, property(func))
    return func

@praxoutput
def utf_8(praxbytes):
    return praxbytes.bytes.decode('utf-8')

@praxoutput
def raw(praxbytes):
    return praxbytes.bytes.decode('latin-1')

@praxoutput
def num(praxbytes):
    return int_from_bytes(praxbytes.bytes, 'big')

@praxfunction
def H(pb):
    pb = PraxBytes(pb)
    return PraxBytes(binascii.hexlify(pb.bytes))


@praxfunction
def h(pb):
    pb = PraxBytes(pb)
    return PraxBytes(binascii.unhexlify(pad_even(pb.bytes)))


@praxfunction
def e(pb, num_bytes=4):
    """
    Swaps endianness
    @param pb: input
    @param num_bytes: number of bytes to use when swapping endianness
    @return: PB of swapped bytes
    """
    pb = PraxBytes(pb)
    byteswap = bytearray(len(pb.bytes))
    for i in range(num_bytes):
        byteswap[i::num_bytes] = pb.bytes[num_bytes-1-i::num_bytes]
    return PraxBytes(byteswap)


@praxfunction
def f(pb):
    pb = PraxBytes(pb)
    return PraxBytes(open(pb.raw, 'rb').read())


def stdin():
    return PraxBytes(sys.stdin.read())


@praxfunction
def plusone(pb):
    number = int_from_bytes(pb.bytes)
    return PraxBytes(int_to_bytes(number + 1))


if __name__ == "__main__":
    import IPython
    IPython.embed()
