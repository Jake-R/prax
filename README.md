# pyrax
pyrax is a data conversion utility a la radare2's rax. It allows the user to enter a snippet of data in one format and see it in a number of other formats (hex, decimal, binary, raw, Base 64, etc.) and optionally to apply operators to the raw data (swap endianness currently)

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
