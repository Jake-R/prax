from __future__ import absolute_import, division, print_function
from builtins import *

import os
import sys
import argparse
from inspect import signature, _empty

from prax import *
# for print_funcs #
from prax import core
# end print_funcs #


def print_funcs(module):
    vals = []
    for name in module.__all__:
        attr = getattr(module, name)
        params = ""
        if callable(attr):
            sig = signature(attr)
            params = ", ".join([x.name if x.default is _empty else "{}={}".format(x.name, x.default)
                                for x in sig.parameters.values()])
        description = attr.__doc__.split("\n")[0].strip()
        vals.append(("{name}({params})".format(name=name, params=params), description))
    ret = ""
    for val in vals:
        ret = ret + ("{:<25}:  {}\n".format(*val))
    return ret


description = """A data conversion tool.
Manipulate data by converting python builtins (str, int, bytes) to PraxBytes e.g. p(0xdeadbeef)
Chain conversions and manipulate data using normal operators:
    "A"*10 + h("deadbeef").e().H() -> "AAAAAAAAAAefbeadde"
    f("README.md")[:6] = "# Prax"
    
"""


def main():
    parser = argparse.ArgumentParser(description=description+print_funcs(core),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", "--no_newline", action='store_true', help="Don't add a newline to output.")
    parser.add_argument("input")
    args = parser.parse_args()
    end = "" if args.no_newline else "\n"
    os.write(sys.stdout.fileno(), eval(args.input).bytes)
    print("", end=end)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
