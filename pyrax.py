#!/usr/bin/python

import argparse
import base64
import binascii
import functools
import math
import string
from parsing import parser, semantics
from grako.exceptions import FailedParse


def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


class Formatter(object):
    def __init__(self, check=lambda x: True, strip=lambda x: x, add=lambda x: x):
        self.check = check
        self.strip = strip
        self.add = add


class StartsWith(Formatter):
    def __init__(self, starts_with):
        self.starts_with = starts_with
        super().__init__(check=lambda x: x.startswith(self.starts_with),
                         strip=lambda x: x[len(self.starts_with):],
                         add=lambda x: self.starts_with + x)


class EvenNum(Formatter):
    def __init__(self):
        self.isEven = lambda x: len(x) % 2 == 0
        super().__init__(strip=lambda x: x,
                         add=lambda x: x if self.isEven(x) else '0' + x)


class EndsWith(Formatter):
    def __init__(self, ends_with):
        self.ends_with = ends_with
        super().__init__(check=lambda x: x.endswith(self.ends_with),
                         strip=lambda x: x[:len(self.ends_with)],
                         add=lambda x: x + self.ends_with)


class Operator(object):
    NAME = None
    FLAG = None

    def operate(self, number):
        return number


class SwapEndianness(Operator):
    NAME = 'swap endianness'
    FLAG = 'e'

    @classmethod
    def add_args(cls, parser):
        parser.add_argument("-{}".format(cls.FLAG), action='store_true', default=False,
                            help='Apply "{}" operator to data'.format(cls.NAME))
        return parser

    def operate(self, number: int) -> int:
        def to_byte(x): x.to_bytes(math.ceil(math.log(x, 16) / 2), 'big')

        return int.from_bytes(to_byte(number), 'little')


class Type(object):
    NAME = None
    FLAG = None
    FORMATTERS = []

    @classmethod
    def add_args(cls, parser):
        parser.add_argument("-{}".format(cls.FLAG.lower()), action='store_true', default=False,
                            help="output in {}".format(cls.NAME))
        parser.add_argument("-{}".format(cls.FLAG.upper()), action='store_true', default=False,
                            help="force input as {}".format(cls.NAME))
        return parser

    @classmethod
    def strip_format(cls, string_):
        return string_

    @classmethod
    def add_format(cls, string_):
        return string_

    @classmethod
    def convert(cls, number):
        return cls.add_format(cls._to_str(number))

    @classmethod
    def parse(cls, string_):
        return cls._to_int(cls.strip_format(string_))

    @classmethod
    def _to_int(cls, string_):
        return None

    @classmethod
    def _to_str(cls, number):
        return None


class Base(Type):
    BASE = None
    ALPHABET = string.digits + string.ascii_lowercase

    @classmethod
    def strip_format(cls, string_: str) -> str:
        for fmt in cls.FORMATTERS:
            if fmt.check(string_):
                string_ = fmt.strip(string_)
            else:
                return None
        return string_

    @classmethod
    def add_format(cls, string_):
        for fmt in reversed(cls.FORMATTERS):
            string_ = fmt.add(string_)
        return string_

    @classmethod
    def parse(cls, string_: str, force=False) -> int:
        stripped = cls.strip_format(string_)
        if stripped is not None:  # string_ fits formatting of this type
            return cls._to_int(stripped)
        if force:
            return cls._to_int(string_)
        return None

    @classmethod
    def convert(cls, *args) -> str:
        val = "".join([cls._to_str(x) for x in args])
        return cls.add_format(val)

    @classmethod
    def _to_int(cls, string_):
        try:
            return int(string_, cls.BASE)
        except ValueError:
            return None

    # http://interactivepython.org/courselib/static/pythonds/Recursion/pythondsConvertinganIntegertoastring_inAnyBase.html
    @classmethod
    def _to_str(cls, number: int) -> str:
        if cls.BASE > len(cls.ALPHABET):
            print("too large of a base :(")
            return None
        if number < cls.BASE:
            return cls.ALPHABET[number]
        else:
            return cls._to_str(number // cls.BASE) + cls.ALPHABET[number % cls.BASE]


class BaseHex(Base):
    NAME = 'hex'
    BASE = 16
    FLAG = 'x'
    FORMATTERS = [StartsWith('0x'), EvenNum()]


class BaseDecimal(Base):
    NAME = 'decimal'
    BASE = 10
    FLAG = 'd'


class BaseOctal(Base):
    NAME = 'octal'
    BASE = 8
    FLAG = 'o'
    FORMATTERS = [StartsWith('0o')]


class BaseBinary(Base):
    NAME = 'binary'
    BASE = 2
    FLAG = 'b'
    FORMATTERS = [StartsWith('0b')]


class Ascii(Type):
    NAME = 'ascii'
    FLAG = 'r'

    @classmethod
    def _to_str(cls, *number):
        # convert int -> even numbered hex -> bytes -> raw
        i = "".join([EvenNum().add(BaseHex._to_str(x)) for x in number])
        return binascii.unhexlify(i).decode("latin1")

    @classmethod
    def _to_int(cls, string_):
        if string_ is None:
            return None
        if type(string_) is str:
            string_ = string_.encode('latin-1')
        return BaseHex.parse(binascii.hexlify(string_).decode('latin1'), force=True)


class Base64(Ascii):
    NAME = "Base64"
    FLAG = 's'

    @classmethod
    def strip_format(cls, string_):
        try:
            return base64.b64decode(string_)
        except binascii.Error:
            return None

    @classmethod
    def add_format(cls, string_):
        return base64.b64encode(string_.encode('latin-1')).decode('latin-1')


classes = [BaseHex, BaseDecimal, Ascii, Base64]
operators = [SwapEndianness]


def parse_to_int(string_):
    return [y for y in [x.parse(string_) for x in classes] if y is not None][0]


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("input", nargs='+')
    for x in classes + operators:
        arg_parser = x.add_args(arg_parser)
    args = arg_parser.parse_args()
    args_dict = vars(args)

    input_type = None
    output_type = None
    for x in classes:
        if args_dict[x.FLAG.lower()]:
            output_type = x
        if args_dict[x.FLAG.upper()]:
            input_type = x

    funcs = [x.operate for x in operators if args_dict[x.FLAG]]
    ops = []
    if funcs is not None:
        ops = compose(*funcs)

    argument = " ".join(args.input)
    if output_type is None:
        values = []
        for x in classes:
            p = parser.PyraxParser(semantics=semantics.PyraxSemantics(x, input_type, operators=ops))
            try:
                values.append(x.add_format(p.parse(argument)))
            except FailedParse:
                print("Invalid syntax")
                exit(1)
        for val in values:
            print(val)
    else:
        p = parser.PyraxParser(semantics=semantics.PyraxSemantics(output_type, operators=ops))
        print(output_type.add_format(p.parse(argument)))


if __name__ == "__main__":
    main()
