# Prax
[Prax](http://www.imdb.com/character/ch0566106/) is a data conversion and buffer creation utility inspired by radare2's rax. It allows the user to enter data and manipulate it with a fast and simple Python-based syntax. In fact, it actually is Python! Prax commands can include python features like variables or list comprehensions and any command can be used in a Python script by including `from prax import *`.

## Warning
Prax `eval()`s your input so do not include any unstructed data on the command line (i.e. no command substitution). Instead use Prax functions like `stdin()` or `f()` to work with untrusted data.

# Usage
>> prax -h
usage: prax [-h] [-n] input

A data conversion tool.
Manipulate data by converting python builtins (str, int, bytes) to PraxBytes e.g. p(0xdeadbeef)
Chain conversions and manipulate data using normal operators:
    "A"*10 + h("deadbeef").e().H() -> "AAAAAAAAAAefbeadde"
    f("README.md")[:6] = "# Prax"
    
p(input=)                :  Convert to PraxBytes
H(input)                 :  Convert to hexadecimal representation
B(input)                 :  Convert to binary representation
h(input)                 :  Convert from hexadecimal representation
e(input, num_bytes=4)    :  Swaps endianness. optional param 'num_bytes'
f(input)                 :  Reads contents of a file
stdin()                  :  Reads from stdin

positional arguments:
  input

optional arguments:
  -h, --help        show this help message and exit
  -n, --no_newline  Don't add a newline to output.

# Examples
~~~~
>> prax '"A"*10 + h("deadbeef").e().H()'
AAAAAAAAAAefbeadde
>> prax 'f("README.md")[2:6]'
Prax
~~~~
Python operators are implemented as follows:

Operator | Explanation | Example
--- | --- | ---
e1+e2 | concatenate e1 with e2 | `>> prax 'p("ABCD")+p(0x45464748)' -> ABCDEFGH`
e1\*e2 |repeat e1 e2 times | `>>prax 'p(0x41)*6' -> AAAAAA`
e1\**e2 | repeat e1 e2 times, incrementing by 1 | `>>prax 'p(0x30)**10 -> 0123456789`
e1 <</>> e2 | shift e1 by e2 | `>>prax 'p(0x1).H() + p("  ") + (p(0x1) << 2).H()' -> 01  04`
e1 ==/!= e2 | test for equality | 
e1 &/^/| e2 | bitwise and/xor/or e1 with e2 | 

# Install
~~~~
git clone https://github.com/Jake-R/prax.git
sudo -H pip install -e prax
~~~~

