""""Slim boilerplate cli"""

from typing import NamedTuple, Optional
from collections import ChainMap

__version__ = '0.0.1'


class C(NamedTuple):
    a: str = 'a'
    b: str = 'b'
    x: int = 1


def c(params: Optional[dict] = None, __c=[]) -> C:
    if params is not None:
        __c.append(C(**ChainMap(params, C()._asdict())))
    elif len(__c) == 0:
        __c.append(C())
    return __c[-1]
