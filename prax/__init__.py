from .praxbytes import PraxBytes, PraxException, praxoutput, praxmethod, praxfunction, praxmodule

from prax.modules.core import *
from prax.modules.shellcode import *
from prax.modules.urlmodule import *

import os
import sys
MODULE_DIR = os.path.expanduser("~/.prax/modules")

# search for user added prax modules
if os.path.exists(MODULE_DIR):
    # Folder exists, lets parse and import every .py file
    sys.path.append(MODULE_DIR)
    for (dirpath, dirnames, filenames) in os.walk(MODULE_DIR):
        for fname in filenames:
            if fname.endswith('.py'):
                fname = fname[:-3]
                module = __import__(fname)
                for attr in dir(module):
                    if not attr.startswith('_'):
                        globals()[attr] = getattr(module, attr)
                #with open(module) as f:
                #    code = compile(f.read(), module, 'exec')
                #    exec(code, globals(), locals())


# del os
# del core
