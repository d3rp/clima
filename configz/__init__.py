""""Slim boilerplate cli"""

from typing import NamedTuple
from collections import ChainMap

__version__ = '0.0.1'


class C(NamedTuple):
    a: str = 'a'
    b: str = 'b'
    x: int = 1


def c(new: C = None, __c=[]):
    if new is not None:
        __c.append(new)
    elif len(__c) == 0:
        __c.append(C())
    print(f'c inner: {repr(__c)}')
    return __c[-1]


def configure(**params):
    defaults = C(a='oh')
    _c = C(**dict(ChainMap(params, defaults._asdict())))
    global c
    c(_c)
