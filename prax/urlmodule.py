from __future__ import absolute_import, division, print_function
from builtins import *

from prax import *
import urllib

@praxfunction
@praxmethod
def urlenc(pb):
    """Produce a URL safe encoded string"""
    pb = p(pb)
    return p(urllib.quote_plus(pb.raw))


