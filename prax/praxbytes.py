from __future__ import absolute_import, division, print_function
from builtins import *
from collections import defaultdict
from funcsigs import signature, _empty
import types

from prax.utility import isiterable, int_to_bytes, export, py_major_version, add_func_to_class


class PraxException(BaseException):
    pass


class PraxBytes(object):
    def __init__(self, input=b""):
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

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, item):
        return PraxBytes(self.bytes.__getitem__(item))

    def __contains__(self, item):
        return self.bytes.__contains__(PraxBytes(item).bytes)

    @staticmethod
    def _realapply(left, right, func):
        try:
            return PraxBytes(func(PraxBytes(left), PraxBytes(right)))
        except PraxException:
            return NotImplemented

    # Concatenation (+)
    def _realadd(self, left, right):
        return self._realapply(left, right, lambda x, y: x.bytes + y.bytes)

    def __add__(self, other):
        return self._realadd(self, other)

    def __radd__(self, other):
        return self._realadd(other, self)

    # multiply
    def _realmul(self, left, right):
        return self._realapply(left, right, lambda x, y: x.bytes * y.num)

    def __mul__(self, other):
        return self._realmul(self, other)

    def __rmul__(self, other):
        return self._realmul(other, self)

    # lshift
    def _reallshift(self, left, right):
        return self._realapply(left, right, lambda x, y: x.num << y.num)

    def __lshift__(self, other):
        return self._reallshift(self, other)

    def __rlshift__(self, other):
        return self._reallshift(other, self)

    # rshift
    def _realrshift(self, left, right):
        return self._realapply(left, right, lambda x, y: x.num >> y.num)

    def __rshift__(self, other):
        return self._realrshift(self, other)

    def __rrshift__(self, other):
        return self._realrshift(other, self)

    # rshift
    def _realand(self, left, right):
        return self._realapply(left, right, lambda x, y: x.num & y.num)

    def __and__(self, other):
        return self._realand(self, other)

    def __rand__(self, other):
        return self._realand(other, self)

    # rshift
    def _realxor(self, left, right):
        return self._realapply(left, right, lambda x, y: x.num ^ y.num)

    def __xor__(self, other):
        return self._realxor(self, other)

    def __rxor__(self, other):
        return self._realxor(other, self)

    # rshift
    def _realor(self, left, right):
        return self._realapply(left, right, lambda x, y: x.num | y.num)

    def __or__(self, other):
        return self._realor(self, other)

    def __ror__(self, other):
        return self._realor(other, self)

    # multiply and increase
    @staticmethod
    def _realmatmul(left, right):
        try:
            res = PraxBytes()
            for i in range(PraxBytes(right).num):
                res += PraxBytes(PraxBytes(left).num + i)
            return res
        except PraxException:
            return NotImplemented

    def __matmul__(self, other):
        return self._realmatmul(self, other)

    def __rmatmul__(self, other):
        return self._realmatmul(other, self)

    def __pow__(self, other):
        return self._realmatmul(self, other)

    def __rpow__(self, other):
        return self._realmatmul(other, self)


class PraxModule(object):
    def __init__(self):
        self.outputs = []
        self.methods = []
        self.functions = []
        self.modules = []

    def __str__(self):
        return self._str_list(self.outputs, "outputs") + \
               self._str_list(set(self.methods + self.functions), "methods/functions") + \
               self._str_list(self.modules, "modules", func=self._str_module)

    def _str_base(self, item):
        params = ""
        if item.__doc__ is not None:
            description = item.__doc__.split("\n")[0].strip()
        else:
            description = ""
        if callable(item):
            sig = signature(item)
            params = ", ".join([x.name if x.default is _empty else "{}={}".format(x.name, x.default)
                                for x in sig.parameters.values()])
            return ("{name}({params})".format(name=item.__name__, params=params), description)
        else:
            return item.__name__, description

    def _str_module(self, item):
        return item

    def _str_list(self, list, name, func=None):
        if not func:
            func = self._str_base
        if not list:
            return ""
        return "{}:\n".format(name) + "".join([("\t{:<25}:  {}\n".format(*func(x))) for x in list])


praxmodules = defaultdict(PraxModule)

def praxoutput(func):
    praxmodules[func.__module__].outputs.append(func)
    setattr(PraxBytes, func.__name__, property(func))
    return func


def praxmethod(func):
    praxmodules[func.__module__].methods.append(func)

    return add_func_to_class(func, PraxBytes)


def praxfunction(func):
    praxmodules[func.__module__].functions.append(func)

    export(func)
    return func


def praxmodule(parent, child, description=None):
    parent.__all__.append(child)
    if not description:
        description = getattr(parent, child).__doc__.split("\n")[0]
    praxmodules[parent.__name__].modules.append((child, description))



