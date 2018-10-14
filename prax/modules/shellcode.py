from __future__ import absolute_import, division, print_function
from builtins import *

import sys
from prax import *
from pwnlib import shellcraft as shl
from pwnlib.util.packing import pack, unpack
import pwnlib
import decorator


def _prax_wrap(f, *args, **kw):
    return p(f(*args, **kw))


def prax_wrap(f):
    return decorator.decorate(f, _prax_wrap)


@praxfunction
def set_arch(arch):
    """Set the pwnlib architecture (same as -a for cmd tool)"""
    pwnlib.context.context(arch=arch)


@praxfunction
def binsh(arch=None):
    """assembled binsh shellcode. equivalent to asm(shl.sh())"""
    return p(shl.sh()).asm()


@praxfunction
@praxmethod
def asm(pb, arch=None):
    """Assemble instructions or shellcode according to current arch"""
    pb = p(pb)
    return p(pwnlib.asm.asm(pb.raw, arch=arch))


@praxfunction
@praxmethod
def disasm(pb, arch=None):
    """Disassemble instructions or shellcode according to current arch"""
    pb = p(pb)
    return p(pwnlib.asm.disasm(pb.bytes, arch=arch, byte=False, offset=False))


def _i(f, *args, **kwargs):
    return p(f(p(args[0]).num, *args[1:], **kwargs))


def iwrap(f, name, doc=None):
    f.__module__ = __name__
    f.__name__ = name
    if doc:
        f.__doc__ = doc
    return decorator.decorate(f, _i)

pack = praxfunction(praxmethod(iwrap(pack, 'pack', 'Pack a word sized value according to the specified arch')))
unpack = praxfunction(praxmethod(iwrap(unpack, 'unpack', 'Unpack a word sized value according to the specified arch')))

praxmodule(sys.modules[__name__], "shl")

if __name__ == "__main__":
    import IPython
    IPython.embed()
