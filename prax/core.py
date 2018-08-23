from prax.praxbytes import PraxBytes, praxoutput, praxmethod, praxfunction
from prax.utility import int_from_bytes, int_to_bytes, pad_even
import binascii
import sys


@praxoutput
def utf_8(praxbytes):
    """Decode as utf-8"""
    return praxbytes.bytes.decode('utf-8')


@praxoutput
def raw(praxbytes):
    """Decode as latin-1 (raw)"""
    return praxbytes.bytes.decode('latin-1')


@praxoutput
def num(praxbytes):
    """Decode as int (big-endian)"""
    return int_from_bytes(praxbytes.bytes, 'big')


@praxfunction
def p(input=b""):
    """Convert to PraxBytes"""
    return PraxBytes(input)


@praxfunction
@praxmethod
def H(input):
    """Convert to hexadecimal representation"""
    input = PraxBytes(input)
    return PraxBytes(binascii.hexlify(input.bytes))


@praxfunction
@praxmethod
def b(input):
    """Convert to binary representation"""
    return p(bin(p(input).num)[2:])


@praxfunction
@praxmethod
def h(input):
    """Convert from hexadecimal representation"""
    input = PraxBytes(input)
    return PraxBytes(binascii.unhexlify(pad_even(input.bytes)))


@praxfunction
@praxmethod
def e(input, num_bytes=4):
    """Swaps endianness. optional param 'num_bytes'
    @param input: input
    @param num_bytes: number of bytes to use when swapping endianness
    @return: input of swapped bytes
    """
    input = PraxBytes(input)
    byteswap = bytearray(len(input.bytes))
    for i in range(num_bytes):
        byteswap[i::num_bytes] = input.bytes[num_bytes - 1 - i::num_bytes]
    return PraxBytes(byteswap)


@praxfunction
@praxmethod
def f(input):
    """Reads contents of a file"""
    input = PraxBytes(input)
    return PraxBytes(open(input.raw, 'rb').read())

gStdin = None
@praxfunction
def stdin():
    """Reads from stdin"""
    global gStdin

    if gStdin is None:
        gStdin = PraxBytes(sys.stdin.read())
    
    return gStdin


