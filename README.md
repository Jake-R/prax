# Prax
[Prax](http://expanse.wikia.com/wiki/Praxidike_Meng) is a data conversion and buffer creation utility inspired by radare2's rax. It allows the user to enter data and manipulate it with a fast and simple Python-based syntax. In fact, it actually is Python! Prax commands can include python features like variables or list comprehensions and any command can be used in a Python script by including `from prax import *`.

## Warning!!
Prax `eval()`s your input so do not include any untrusted data on the command line (i.e. no command substitution). Instead use Prax functions like `stdin()` or `f()` to work with untrusted data.

# Examples
~~~~
>> prax '"A"*10 + h("deadbeef").e().H()'
AAAAAAAAAAefbeadde
>> prax 'f("README.md")[2:6]'
Prax

# Simple Buffer overflow example
>> prax --hd 'asm(shl.nop())*40 + asm(shl.sh()) + "A"*47 +i(0xffffce20)'
00000000  90 90 90 90  90 90 90 90  90 90 90 90  90 90 90 90  │····│····│····│····│
*
00000020  90 90 90 90  90 90 90 90  6a 68 68 2f  2f 2f 73 68  │····│····│jhh/│//sh│
00000030  2f 62 69 6e  89 e3 68 01  01 01 01 81  34 24 72 69  │/bin│··h·│····│4$ri│
00000040  01 01 31 c9  51 6a 04 59  01 e1 51 89  e1 31 d2 6a  │··1·│Qj·Y│··Q·│·1·j│
00000050  0b 58 cd 80  41 41 41 41  41 41 41 41  41 41 41 41  │·X··│AAAA│AAAA│AAAA│
00000060  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
*
00000080  41 41 41 20  ce ff ff                               │AAA │···│
00000087
~~~~

# Usage
~~~~
usage: praxcmd.py [-h] [-n] [-d] [-a ARCH] [--hd] input

A buffer building and data manipulation tool.
Manipulate data by converting python builtins (str, int, bytes) to PraxBytes e.g. p(0xdeadbeef)
Chain conversions and manipulate data using normal operators:
    "A"*10 + h("deadbeef").e().H() -> "AAAAAAAAAAefbeadde"
    f("README.md")[:6] = "# Prax"

core
outputs:
        utf_8(praxbytes)         :  Decode as utf-8
        raw(praxbytes)           :  Decode as latin-1 (raw)
        num(praxbytes)           :  Decode as int (big-endian)
        hd(praxbytes)            :  Hexdump
methods/functions:
        h(input)                 :  Convert from hexadecimal representation
        B(input)                 :  Convert to binary representation
        H(input)                 :  Convert to hexadecimal representation
        e(input, num_bytes=4)    :  Swaps endianness. optional param 'num_bytes'
        b(input)                 :  Convert from binary representation
        f(input)                 :  Reads contents of a file
        p(input=b'')             :  Convert to PraxBytes
        stdin()                  :  Reads from stdin

shellcode
methods/functions:
        binsh(arch=None)         :  assembled binsh shellcode. equivalent to asm(shl.sh())
        asm(pb, arch=None)       :  Assemble instructions or shellcode according to current arch
        disasm(pb, arch=None)    :  Disassemble instructions or shellcode according to current arch
        i(number, word_size=None, endianness=None, sign=None, kwargs):  Pack a word sized value according to the specified arch
        set_arch(arch)           :  Set the pwnlib architecture (same as -a for cmd tool)
        ui(data, word_size=None) :  Unpack a word sized value according to the specified arch
modules:
        shl                      :  The shellcode module.

urlmodule
methods/functions:
        urlenc(pb)               :  Produce a URL safe encoded string

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -n, --no_newline      Don't add a newline to output.
  -d, --debug           launch idpb when running command
  -a ARCH, --arch ARCH  set pwnlib architecture
  --hd                  output as hexdump


~~~~

Python operators are implemented as follows:

Operator | Explanation | Example
--- | --- | ---
e1+e2 | concatenate e1 with e2 | `>> prax 'p("ABCD")+p(0x45464748)' -> ABCDEFGH`
e1\*e2 |repeat e1 e2 times | `>>prax 'p(0x41)*6' -> AAAAAA`
e1\**e2 | repeat e1 e2 times, incrementing by 1 | `>>prax 'p(0x30)**10 -> 0123456789`
e1 <</>> e2 | shift e1 by e2 | `>>prax 'p(0x1).H() + p("  ") + (p(0x1) << 2).H()' -> 01  04`
e1 ==/!= e2 | test for equality | 
e1 &/^/\| e2 | bitwise and/xor/or e1 with e2 | 


# Install
Prax supports Python 2 and 3 but depends on pwntools which is a Python 2 project. Github user 'arthaud' maintains a Python 3 branch but it is two years out of date as of August 2018.  Things seem to work okay but the pwntools integration is not rigorously tested on Python3. Use at your own risk.
~~~~
git clone https://github.com/Jake-R/prax.git
# Python 2
sudo -H pip install -e prax
# Python3
sudo -H pip3 install -e . --find-links git+https://github.com/arthaud/python3-pwntools.git#egg=pwntools-100.0.0 pwntools
~~~~


# Custom functions
Users can extend Prax through the use of the ~/.prax/modules directory. Any Python file in this directory will be loaded as a Prax module. Prax offers a couple of decorators to make it easy to add functions, methods, outputs, and modules to Prax.

## @praxfunction
Prax functions are functions that take 0 or more arguments and return a PraxBytes object. Praxfunctions should always call p() on their inputs to convert them to PraxBytes in the case that the user passed a Python primitive rather than the result of a previous Prax operation. If the input is a PraxBytes object then p() will return the object unchanged.
```python
from prax import *
@praxfunction
def asdf():
    """returns 'asdf'"""
    return p("asdf")
```

## @praxmethod
Prax methods are functions that take one or more arguments and return a PraxBytes object. Prax methods are patched into the PraxBytes class so that operations can be chained. Most Prax methods should also be Prax functions and decorated as such.
```python
from prax import *
@praxfunction
@praxmethod
def reverse(input_):
    """reverses the input"""
    return p(input_)[::-1]

p("asdf").reverse()
# or
reverse("asdf")
```

## @praxoutput
Prax outputs are attribute functions that convert from a PraxBytes object to a native python object.
```python
from prax import *
@praxoutput
def utf_8(praxbytes):
     """Decode as utf-8"""
     return praxbytes.bytes.decode('utf-8')"
p("asdf").utf_8
```

## praxmodule
Prax modules are cases where you want to pass an entire module into the prax context, optionally under a different name. This is used for the shellcraft module of pwntools.
```python
from prax import *
from pwntools import shellcraft as shl
# pass in current module and name of imported module as string
praxmodule(sys.modules[__name__], "shl")
```

