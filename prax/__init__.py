from .praxbytes import PraxBytes, PraxException, praxoutput, praxfunction
### delete ###
from prax import praxbytes
### end delete ###

p = PraxBytes

for x in praxbytes.funcs:
    globals()[x.__name__] = x


del praxbytes


if __name__ == "__main__":
    import IPython
    IPython.embed()
