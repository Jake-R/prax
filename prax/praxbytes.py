from __future__ import absolute_import, division, print_function
from builtins import (bytes, int, str)
import types

from prax.utility import isiterable, int_to_bytes, export, py_major_version, add_method

funcs = []


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


def praxoutput(func):
    setattr(PraxBytes, func.__name__, property(func))
    return func


def praxfunction(func):
    if py_major_version() < 3:
        setattr(PraxBytes, func.__name__, types.MethodType(func, None, PraxBytes))
    else:
        setattr(PraxBytes, func.__name__, func)
    funcs.append(func)
    praxexport(func)
    return func


def praxexport(func):
    export(func)
    return func


if __name__ == "__main__":
    import IPython
    IPython.embed()
