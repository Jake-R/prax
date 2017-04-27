# pyrax
pyrax is a data conversion utility a la radare2's rax. It allows the user to enter a snippet of data in one format and see it in a number of other formats (hex, decimal, binary, raw, Base 64, etc.) and optionally to apply operators to the raw data (swap endianness currently)

# Examples
~~~~
>> ./pyrax.py 0xdeadbeef
0xdeadbeef 3735928559 Þ­¾ï 3q2+7w==

>> ./pyrax.py -r 0xdeadbeef 
Þ­¾ï

>> ./pyrax.py -e 0xdeadbeef
0xefbeadde 4022250974 ï¾­Þ 776t3g==

>> ./pyrax.py ABCD 0xcafe 12345678
0x41424344 1094861636 ABCD QUJDRA==
0xcafe 51966 Êþ yv4=
0xbc614e 12345678 ¼aN vGFO

# When specifying output format the args are concatenated
>> ./pyrax.py -r ABCD 0x45464748 IJKL
ABCDEFGHIJKL
~~~~

# Usage
~~~~
>> ./pyrax.py -h
usage: pyrax.py [-h] [-x] [-X] [-d] [-D] [-r] [-R] [-s] [-S] [-e]
                input [input ...]

positional arguments:
  input

optional arguments:
  -h, --help  show this help message and exit
  -x          output in hex
  -X          force input as hex
  -d          output in decimal
  -D          force input as decimal
  -r          output in ascii
  -R          force input as ascii
  -s          output in Base64
  -S          force input as Base64
  -e          Apply "swap endianness" operator to data
~~~~
