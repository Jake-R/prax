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
Python operators are implemented as follows:

Operator | Explanation | Example
--- | --- | ---
e1+e2 | concatenate e1 with e2 | `>> prax 'p("ABCD")+p(0x45464748)' -> ABCDEFGH`
e1\*e2 |repeat e1 e2 times | `>>prax 'p(0x41)*6' -> AAAAAA`
e1\**e2 | repeat e1 e2 times, incrementing by 1 | `>>prax 'p(0x30)**10 -> 0123456789`
e1 <</>> e2 | shift e1 by e2 | `>>prax 'p(0x1).H() + p("  ") + (p(0x1) << 2).H()' -> 01  04`
e1 ==/!= e2 | test for equality | 
e1 &/^/\| e2 | bitwise and/xor/or e1 with e2 | 


# Usage
~~~~
usage: prax [-h] [-n] [-d] [-a ARCH] [--hd] input

A buffer building and data manipulation tool.
Manipulate data by converting python builtins (str, int, bytes) to PraxBytes e.g. p(0xdeadbeef)
Chain conversions and manipulate data using normal operators:
    "A"*10 + h("deadbeef").e().H() -> "AAAAAAAAAAefbeadde"
    f("README.md")[:6] = "# Prax" 
    asm(shl.nop())*40 + asm(shl.sh()) + "A"*47 + i(0xffffce20) -> 
        nopsled       +   shellcode   + filler + return addr overwrite

prax.core:
	p(input=)                :  Convert to PraxBytes
	h(input)                 :  Convert from hexadecimal representation
	H(input)                 :  Convert to hexadecimal representation
	b(input)                 :  Convert from binary representation
	B(input)                 :  Convert to binary representation
	e(input, num_bytes=4)    :  Swaps endianness. optional param 'num_bytes'
	f(input)                 :  Reads contents of a file
	stdin()                  :  Reads from stdin

prax.shellcode:
	set_arch(arch)           :  Set the pwnlib architecture (same as -a for cmd tool)
	binsh(arch=None)         :  assembled binsh shellcode. equivalent to asm(shl.sh())
	asm(pb, arch=None)       :  Assemble instructions or shellcode according to current arch
	disasm(pb, arch=None)    :  Disassemble instructions or shellcode according to current arch
	i(number, word_size=None, endianness=None, sign=None, kwargs):  Pack a word sized value according to the specified arch
	ui(a, kw)                :  Unpack a word sized value according to the specified arch
	shl                      :  The shellcode module.

prax.urlmodule:
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

# Install
Prax supports Python 2 and 3 but depends on pwntools which is a Python 2 project. Github user 'arthaud' maintains a Python 3 branch but it is two years out of date as of August 2018.  Things seem to work okay but the pwntools integration is not rigorously tested on Python3. Use at your own risk.
~~~~
git clone https://github.com/Jake-R/prax.git
# Python 2
sudo -H pip install -e prax
# Python3
sudo -H pip3 install -e . --find-links git+https://github.com/arthaud/python3-pwntools.git#egg=pwntools-100.0.0 pwntools
~~~~

