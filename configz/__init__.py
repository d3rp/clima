""""Slim boilerplate for cli scripts"""

from typing import NamedTuple, Optional, TypeVar, Generic, NewType  # , NoneType
from collections import ChainMap, OrderedDict
import inspect
import configparser
from pathlib import Path
from fire import Fire
from functools import lru_cache

__version__ = '0.0.1'

C = TypeVar('C', NamedTuple, type(None))


def filter_config_fields(d: dict, nt):
    return {k: v for k, v in d.items() if k in nt._fields}


def get_config_file(_filepath='test.cfg'):
    filepath = Path(_filepath)
    if not filepath.exists():
        return {}

    file_config = configparser.ConfigParser()
    file_config.read(filepath)
    return dict(file_config['Default'])


# TODO: Requires some metaclass magic to return a class of a type that isn't yet defined here
class Configurable:
    this: C = None

    def __call__(self, params: dict, Conf: C):
        conf = NewType('conf', C)
        self.this = conf(dict(ChainMap(
            params,
            # filter_config_fields(get_config_file(), conf()),
            # filter_config_fields(os.environ, conf()),
            Conf._asdict()
        )))
        self.__annotations__.update({'foo': 'bar'})

    def __getattr__(self, item):
        return self.this[item]

c = Configurable()


# def c(params: dict = None, Conf: C = None, *, __c=[]) -> C:
#     conf = NewType('conf', C)
#     # print(type(conf))
#     # print(params)
#     if params is not None:
#         __c.append(conf(dict(ChainMap(
#             params,
#             # filter_config_fields(get_config_file(), conf()),
#             # filter_config_fields(os.environ, conf()),
#             Conf._asdict()
#         ))))
#     elif len(__c) == 0:
#         __c.append(conf())
#     return __c[-1]


def prepare_signatures(cls, nt: NamedTuple):
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
            for field in nt._fields
        ]
        sig = inspect.signature(method)
        method.__signature__ = sig.replace(parameters=[
            inspect.Parameter(name='self', kind=inspect._VAR_KEYWORD),
            *params
        ])


def prepare(cls, nt: NamedTuple):
    prepare_signatures(cls, nt)
    wrap_method_docs(cls, nt)
    Fire(cls)


def wrap_method_docs(cls: object, nt):
    methods = [m.object for m in inspect.classify_class_attrs(cls) if m.kind == 'method' and not m.name.startswith('_')]
    for m in methods:
        Doc.prepare_doc(nt, m)


class Doc:
    @staticmethod
    def params_with_defs(N):
        params_with_definitions = tuple(
            tuple(
                str(arg_and_def).strip()
                for arg_and_def in src_line.split(':')
            )
            for src_line in inspect.getsourcelines(N.__class__)[0]
            if src_line.startswith(' ')
        )
        return OrderedDict(params_with_definitions)

    @staticmethod
    @lru_cache(128)
    def attr_map(N):
        _attr_map = {}
        for param, _def in Doc.params_with_defs(N).items():
            _type, def_desc = _def.split('=')
            _type = _type.strip()

            # print(def_desc)
            default, description = def_desc.split('#')
            default = default.strip()
            description = description.strip()

            _attr_map.update(
                {
                    param: {
                        'type': _type,
                        'default': default,
                        'description': description,
                    }
                }
            )
        return _attr_map

    @staticmethod
    def prepare_doc(N, f):
        ps_doc = []
        for attr_name, cls in N.__annotations__.items():
            # print(f'"{attr_name}"')
            attr = Doc.attr_map(N).get(attr_name)
            if attr is None:
                # print('skipping')
                continue

            ps_doc.append(f'    --{attr_name} ({attr["type"]}): {attr["description"]} (Default is {attr["default"]})')

        ps_doc = '\n'.join(ps_doc)
        doc = f.__doc__
        doc += '\nArgs:\n' + ps_doc
        # print(repr(f))
        f.__doc__ = doc
