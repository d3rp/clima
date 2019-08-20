""""Slim boilerplate for cli scripts"""

from typing import NamedTuple, Optional, TypeVar, Generic, NewType  # , NoneType
from collections import ChainMap, OrderedDict
import inspect
import configparser
from pathlib import Path
from fire import Fire
from functools import lru_cache
import os

__version__ = '0.0.2'

C = TypeVar('C', bound=NamedTuple)

root = Path.cwd()


def filter_fields(d: dict, nt):
    res = {}
    for k, v in d.items():
        if k in nt._fields:
            res.update({k: v})

    return res


def is_in_module(f):
    return len(list(Path(f).parent.glob('__init__.py')))


def cfgs_gen(f):
    yield from Path(f).parent.glob('*.cfg')


def find_cfg(f):
    f = Path(f)
    cfgs = list(cfgs_gen(f))
    if len(cfgs) == 0:
        if is_in_module(f):
            return find_cfg(f.parent)
        else:
            return None
    else:
        return cfgs[0]


def read_config(_filepath='test.cfg') -> dict:
    filepath = Path(_filepath)
    if not filepath.exists():
        return {}

    file_config = configparser.ConfigParser()
    file_config.read(filepath)
    return dict(file_config['Default'])


state = {
    'schema': None,
    'generated': None,
}


def schema(cls):
    # c: type(cls) = c
    state['schema'] = cls()

    return cls


def cli(cls):
    class Generated(cls, metaclass=Foo):
        def __init__(self, **cli_args):
            c(cli_args, state['schema'])

    state['generated'] = Generated
    init()
    return Generated


def init():
    prepare(state['generated'], state['schema'])


class Foo(type):
    def __new__(cls, name, bases, nmspc):
        # pprint(name)
        # pprint(bases)
        # pprint(nmspc)
        return super().__new__(cls, name, bases, nmspc)

    def __init__(cls, name, bases, nmspc):
        # print('oh hi')
        pass


class Configurable:
    # configured: NewType('conf', C) = None
    configured: C = None

    def __initialize(self, params: dict, configuration_tuple: Generic[C]) -> C:
        config_file = self.__get_config_path(configuration_tuple)
        if config_file is not None:
            config_dict = filter_fields(read_config(config_file), configuration_tuple),
        else:
            config_dict = {}

        configuration = NewType('conf', C)
        self.configured = configuration(dict(ChainMap(
            params,
            config_dict[0],
            filter_fields(os.environ, configuration_tuple),
            configuration_tuple._asdict()
        )))

        return self.configured

    # def __call__(self, params: dict = None, configuration_tuple: Generic[C] = None) -> C:
    def __call__(self, a=None, b=None):
        is_initializing = (a is not None and b is not None)
        if is_initializing:
            # print('initializing')
            return self.__initialize(a, b)

        is_decorating = (a is not None and b is None)
        if is_decorating:
            # print(f'decorating:')
            is_schema = any(_cls is tuple for _cls in inspect.getmro(a))
            if is_schema:
                # print(f'schema: {inspect.getmro(a)}')
                return schema(a)
            else:
                # print('cli')
                return cli(a)

    def __get_config_path(self, configuration_tuple):
        client_file = Path(inspect.getfile(configuration_tuple.__class__))
        if hasattr(configuration_tuple, 'cwd'):
            p = Path(configuration_tuple._asdict()['cwd'])
            if not p.absolute():
                p = client_file / p
        else:
            p = client_file
        config_file = find_cfg(p)

        return config_file

    def __repr__(self):
        return repr(self.configured)

    def __getattr__(self, item):
        res = None
        if self.configured is not None:
            res = self.configured[item]

        return res


def configuration_factory(template: C) -> C:
    cls_attrs = dict(
        __slots__=template.__slots__,
        __init__=template.__init__,
        __repr__=template.__repr__,
    )
    return type('conf', (object,), cls_attrs)


c = Configurable()


# Alternative to call c() for the configuration
# def c(params: dict = None, Conf: Generic[C] = None, *, __c=[]) -> C:
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


def prepare_signatures(cls, nt: C):
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


# TODO: pass class instead of instance
def prepare(cls, nt: C):
    prepare_signatures(cls, nt)
    wrap_method_docs(cls, nt)
    # c()

    # __c(Doc.params_with_defs(nt), nt)
    # __c.configured = configuration_factory(nt)

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

            if '#' in def_desc:
                default, description = def_desc.split('#')
                default = default.strip()
                description = description.strip()
            else:
                default = def_desc.strip()
                description = ''

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
        doc = (doc if doc is not None else '') + '\nArgs:\n' + ps_doc
        # print(repr(f))
        f.__doc__ = doc
