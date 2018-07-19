import sys
from functools import wraps


def export(f):
    """Use a decorator to avoid retyping function/class names.

    * Based on an idea by Duncan Booth:
      http://groups.google.com/group/comp.lang.python/msg/11cbb03e09611b8a
    * Improved via a suggestion by Dave Angel:
      http://groups.google.com/group/comp.lang.python/msg/3d400fb22d8a42e1
    """
    mod = sys.modules[f.__module__]
    if hasattr(mod, '__all__'):
        name, all_ = f.__name__, mod.__all__
        if name not in all_:
            all_.append(name)
    else:
        mod.__all__ = [f.__name__]
    return f


def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator


def isiterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def int_from_bytes(bytes_, endianness='big'):
    return int.from_bytes(bytes_, endianness)


def int_to_bytes(int_, endianness='big'):
    """Helper to convert int to properly sized bytes object"""
    return int_.to_bytes((int_.bit_length() + 7) // 8, endianness)


def pad_even(input_, padding='0'):
    if len(input_) % 2 != 0:
        return b'0' + input_
    return input_


def py_major_version():
    return sys.version_info[0]