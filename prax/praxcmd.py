from __future__ import absolute_import, division, print_function
from builtins import *

import os
import sys
import argparse
from funcsigs import signature, _empty
from prax import *
# for print_funcs #


# end print_funcs #


def print_funcs(module):
    vals = []
    for name in module.__all__:
        attr = getattr(module, name)
        params = ""
        if attr.__doc__ is not None:
            description = attr.__doc__.split("\n")[0].strip()
        else:
            description = ""
        if callable(attr):
            sig = signature(attr)
            params = ", ".join([x.name if x.default is _empty else "{}={}".format(x.name, x.default)
                                for x in sig.parameters.values()])
            vals.append(("{name}({params})".format(name=name, params=params), description))
        else:
            vals.append((name, description))
    ret = "\n{}:\n".format(module.__name__)
    for val in vals:
        ret = ret + ("\t{:<25}:  {}\n".format(*val))
    return ret


description = """A data conversion tool.
Manipulate data by converting python builtins (str, int, bytes) to PraxBytes e.g. p(0xdeadbeef)
Chain conversions and manipulate data using normal operators:
    "A"*10 + h("deadbeef").e().H() -> "AAAAAAAAAAefbeadde"
    f("README.md")[:6] = "# Prax" 
""" + \
              print_funcs(core) + \
              print_funcs(shellcode) + \
              print_funcs(urlmodule)

def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", "--no_newline", action='store_true', help="Don't add a newline to output.")
    parser.add_argument("-d", "--debug", action='store_true', help="launch idpb when running command")
    parser.add_argument("-a", "--arch", default='i386', help="set pwnlib architecture")
    parser.add_argument("input")
    args = parser.parse_args(args)
    set_arch(args.arch)
    end = "" if args.no_newline else "\n"
    if args.input:
        try:
            if args.debug:
                import ipdb
                res = p(ipdb.runeval(args.input)).bytes
            else:
                res = p(eval(args.input)).bytes
            os.write(sys.stdout.fileno(), res)
        except SyntaxError as e:
            print("Invalid input: {}\n{}".format(args.input, e.msg))
    print("", end=end)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
