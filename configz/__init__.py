""""Slim boilerplate cli"""

from typing import NamedTuple, Optional
from collections import ChainMap
import inspect
import os
import configparser
from pathlib import Path

__version__ = '0.0.1'


class C(NamedTuple):
    a: str = 'a'
    b: str = 'b'
    x: int = 1
    y: int = 0


def filter_config_fields(d: dict):
    return {k: v for k, v in d.items() if k in C._fields}


def get_config_file(_filepath='test.cfg'):
    filepath = Path(_filepath)
    if not filepath.exists():
        return {}

    config = configparser.ConfigParser()
    config.read(filepath)
    return dict(config['Default'])


def c(params: Optional[dict] = None, *, __c=[]) -> C:
    if params is not None:
        __c.append(C(**ChainMap(
            params,
            filter_config_fields(get_config_file()),
            filter_config_fields(os.environ),
            C()._asdict(),
        )))
    elif len(__c) == 0:
        __c.append(C())
    return __c[-1]


def prepare_signatures(cls, T: NamedTuple = C):
    """Uses the implicit Configuration NamedTuple's fields as the
    classes methods' signatures i.e. helps fire to show up the
    named tuple's arguments instead of a generic "**params" for the
    subcommands on command line.

    Works in-place, returns None
    """
    methods = {
        k: v for k, v in cls.__dict__.items()
        if not k.startswith('_')
    }
    for m_name, method in methods.items():
        params = [
            inspect.Parameter(name=field, kind=inspect._VAR_KEYWORD)
            for field in T._fields
        ]
        sig = inspect.signature(method)
        method.__signature__ = sig.replace(parameters=[
            inspect.Parameter(name='self', kind=inspect._VAR_KEYWORD),
            *params
        ])
