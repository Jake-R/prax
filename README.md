# pyrax
pyrax is a data conversion utility a la radare2's rax. It allows the user to enter a snippet of data in one format and see it in a number of other formats (hex, decimal, binary, raw, Base 64, etc.) and optionally to apply operators to the raw data (swap endianness currently)

# Examples
pyrax has two primary modes. The first is when no output format is specified. pyrax allows you to see all the permutations of the input(s):
~~~~
>> ./pyrax.py 0xdeadbeef
0xdeadbeef 3735928559 Þ­¾ï 3q2+7w==

>> ./pyrax.py -e 0xdeadbeef
0xefbeadde 4022250974 ï¾­Þ 776t3g==

>> ./pyrax.py ABCD 0xcafe 12345678
0x41424344 1094861636 ABCD QUJDRA==
0xcafe 51966 Êþ yv4=
0xbc614e 12345678 ¼aN vGFO
~~~~

The second mode is when an output format is specified. The argument is parsed using the following rules:
Rule|Explanation|Example
e1+e2|concatenate e1 with e2|'>>pyrax -r ABCD+0x45464748 -> ABCDEFGH'
e1*e2|repeat e1 e2 times|'>>pyrax -x 0x41*6 -> 0x414141414141'
e1@e2|repeat e1 e2 times, incrementing by 1|'>>pyrax -r 0x30@10 -> 0123456789'
(e1)|evaluate as subexpression|'>>pyrax -r '(A*4)@5' -> AAAAAAABAAACAAADAAAE'

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

# Install
~~~~
git clone https://github.com/Jake-R/pyrax.git
sudo -H pip install -e pyrax
~~~~
this will add both 'pyrax' and 'rax' executables to your path (because who has time to type 5 characters when you could type 3).
