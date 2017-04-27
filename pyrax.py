#!/usr/bin/env python

import sys
import argparse
import binascii
import string
import math
import functools
import base64

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

class Formatter(object):
    def __init__(self, check = lambda x:True, strip = lambda x: x, add = lambda x: x):
        self.check = check
        self.strip = strip
        self.add = add

class StartsWith(Formatter):
    def __init__(self, starts_with):
        self.starts_with = starts_with
        super().__init__(check = lambda x: x.startswith(self.starts_with),
                         strip = lambda x: x[len(self.starts_with):],
                         add = lambda x: self.starts_with + x)

class EvenNum(Formatter):
    def __init__(self):
        self.isEven = lambda x: len(x)%2 == 0
        super().__init__(strip = lambda x: x,
                         add = lambda x: x if self.isEven(x) else '0'+x)

class EndsWith(Formatter):
    def __init__(self, ends_with):
        self.ends_with = ends_with
        super().__init__(check = lambda x: x.endswith(self.ends_with),
                         strip = lambda x: x[:len(self.ends_with)],
                         add = lambda x: x + self.ends_with)

class Operator(object):
    NAME = None
    FLAG = None

class SwapEndianness(Operator):
    NAME = 'swap endianness'
    FLAG = 'e'
    def operate(input: int) -> int:
        to_byte = lambda x: x.to_bytes(math.ceil(math.log(x, 16) / 2), 'big')
        return int.from_bytes(to_byte(input), 'little')


class Type(object):
    Name = None
    FLAG = None
    @classmethod
    def strip_format(cls, input):
        return input


class base_generic(Type):
    BASE = None
    FORMATTERS = []
    ALPHABET = string.digits + string.ascii_lowercase
    @classmethod
    def strip_format(cls, input: str) -> str:
        for fmt in cls.FORMATTERS:
            if fmt.check(input):
                input = fmt.strip(input)
            else:
                return None
        return input

    @classmethod
    def parse(cls, input: str, force=False) -> int:
        stripped = cls.strip_format(input)
        if stripped is not None:  # string fits formatting of this type
            return cls._to_int(stripped)
        if force:
            return cls._to_int(input)
        return None

    @classmethod
    def convert(cls, *args) -> str:
        val="".join([cls._from_int(x) for x in args])
        for fmt in reversed(cls.FORMATTERS):
            val = fmt.add(val)
        return val

    @classmethod
    def _to_int(cls, input):
            try:
                return int(input, cls.BASE)
            except ValueError:
                return None

    # http://interactivepython.org/courselib/static/pythonds/Recursion/pythondsConvertinganIntegertoaStringinAnyBase.html
    @classmethod
    def _from_int(cls, input: int) -> str:
        if cls.BASE > len(cls.ALPHABET):
            print("too large of a base :(")
            return None
        if input < cls.BASE:
            return cls.ALPHABET[input]
        else:
            return cls._from_int(input//cls.BASE) + cls.ALPHABET[input % cls.BASE]


class base_hex(base_generic):
    NAME = 'hex'
    BASE = 16
    FLAG = 'x'
    FORMATTERS = [StartsWith('0x'), EvenNum()]

class base_decimal(base_generic):
    NAME = 'decimal'
    BASE = 10
    FLAG = 'd'
class base_octal(base_generic):
    NAME = 'octal'
    BASE = 8
    FLAG = 'o'
    FORMATTERS = [StartsWith('0o')]

class base_binary(base_generic):
    NAME = 'binary'
    BASE = 2
    FLAG = 'b'
    FORMATTERS = [StartsWith('0b')]

class base_64(object):
    NAME="Base64"
    FLAG = 's'
    @classmethod
    def parse(cls, input, force=False):
        try:
            return Ascii.parse(base64.b64decode(input))
        except TypeError:
            raise
    @classmethod
    def convert(cls, *input):
        val = "".join([Ascii.convert(x) for x in input])
        return base64.b64encode(val)

class Ascii(object):
    NAME = 'ascii'
    FLAG = 'r'
    @classmethod
    def strip_format(cls, input: str) -> str:
        return input

    @classmethod
    def parse(cls, input: str, force=False) -> int:
        return base_hex.parse(binascii.hexlify(input.encode('latin1')).decode('latin1'), force = True)

    @classmethod
    def convert(cls, *input) -> str:
        # convert int -> even numbered hex -> bytes -> raw
        i = "".join([EvenNum().add(base_hex._from_int(x)) for x in input])
        return binascii.unhexlify(i).decode("latin1")

def main():
    classes = [base_hex, base_decimal, Ascii, base_64]
    operators = [SwapEndianness]

    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs='+')
    for x in classes:
        parser.add_argument("-{}".format(x.FLAG.lower()), action='store_true', default=False,
                            help="output in {}".format(x.NAME))
        parser.add_argument("-{}".format(x.FLAG.upper()), action='store_true', default=False,
                            help="force input as {}".format(x.NAME))
    for x in operators:
        parser.add_argument("-{}".format(x.FLAG), action='store_true', default=False,
                            help='Apply "{}" operator to data')
    args = parser.parse_args()
    args_dict = vars(args)
    input = None
    output = None
    for x in classes:
        if args_dict[x.FLAG.lower()]:
            output = x
        if args_dict[x.FLAG.upper()]:
            input = x
    values = []

    for in_value in args.input:
        if input is None:
            val = [y for y in [x.parse(in_value) for x in classes] if y is not None][0]
            values.append(val)
        else:
            values.append(input.parse(in_value, force=True))
    funcs = [x.operate for x in operators if args_dict[x.FLAG]]
    if funcs is not None:
        ops = compose(*funcs)
        values = [ops(val) for val in values]

    if output is None:
        for val in values:
            print(" ".join([x.convert(val) for x in classes if x is not input]))
    else:
        print(output.convert(*values), end="")


if __name__ == "__main__":
    main()
