from __future__ import absolute_import, division, print_function

import os
import argparse
import sys
import ast
from funcsigs import signature, _empty
from prax import *
from prax.utils import raw_print
from pyparsing import quotedString
from pwnlib.util.fiddling import hexdump
from collections import OrderedDict


# https://stackoverflow.com/questions/12698028/why-is-pythons-eval-rejecting-this-multiline-string-and-how-can-i-fix-it
def multiline_eval(expr, context):
    """Evaluate several lines of input, returning the result of the last line"""
    tree = ast.parse(expr)
    eval_expr = ast.Expression(tree.body[-1].value)
    exec_expr = ast.Module(tree.body[:-1])
    exec(compile(exec_expr, 'file', 'exec'), context)
    return eval(compile(eval_expr, 'file', 'eval'), context)


description = """A buffer building and data manipulation tool.
Manipulate data by converting python builtins (str, int, bytes) to PraxBytes e.g. p(0xdeadbeef)
Chain conversions and manipulate data using normal operators:
    "A"*10 + h("deadbeef").e().H() -> "AAAAAAAAAAefbeadde"
    f("README.md")[:6] = "# Prax"\n 
""" + praxhelp(['core', 'shellcode'], _ret=True) + \
    "\nTo view the full list of Prax modules run \"prax 'praxhelp()'\""


def complete(string_):
    import IPython
    completer = IPython.core.completer.Completer(locals(), globals())
    completer.limit_to__all__ = True
    completions = set()
    esc = quotedString.suppress().transformString(string_)
    for quote in ["'", '"']:
        if quote in esc:
            # probably didn't close bash escape quotes
            # try removing first char and see if it goes away lol
            string_ = string_[1:]
            break
    for val in xrange(999):
        comp = completer.complete(string_, val)
        if comp is None:
            break
        if comp[len(string_):].startswith("_"):
            continue
        completions.add(comp)
    return " ".join(completions)



def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", "--no_newline", action='store_true', help="Don't add a newline to output.")
    parser.add_argument("-d", "--debug", action='store_true', help="launch idpb when running command")
    parser.add_argument("-a", "--arch", default='i386', help="set pwnlib architecture")
    parser.add_argument("--hd", action='store_true', help="output as hexdump")
    parser.add_argument("input")
    args = parser.parse_args(args)
    set_arch(args.arch)
    end = "" if args.no_newline else "\n"
    if args.input:
        try:
            if args.debug:
                import ipdb
                res = p(ipdb.runeval(args.input, globals=globals(), locals=locals()))
            else:
                res = p(multiline_eval(args.input, globals()))
            if args.hd:
                print(res.hd)
            else:
                raw_print(res.bytes)
        except SyntaxError as e:
            print("Invalid input: {}\n{}".format(args.input, e.msg))
            return 1
    print("", end=end)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
