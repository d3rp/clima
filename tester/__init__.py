from typing import NamedTuple
from configz import Configurable


class Configuration(NamedTuple):
    a: str = 'a'  # a description
    b: str = 'b'  # b description
    x: int = 1  # x description
    y: int = 0  # y description


c: Configuration = Configurable()
c({}, Configuration())
