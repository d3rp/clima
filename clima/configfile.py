"""Configuration file (sth.cfg) handling"""
import configparser
import inspect
from pathlib import Path


def is_in_module(f):
    return len(list(Path(f).parent.glob('__init__.py')))


def cfgs_gen(p):
    yield from Path(p).parent.glob('*.cfg')


def find_cfg(p):
    p = Path(p)
    cfgs = list(cfgs_gen(p))
    if len(cfgs) == 0:
        if is_in_module(p):
            return find_cfg(p.parent)
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
    if 'Default' in file_config:
        return dict(file_config['Default'])
    else:
        print('warning: config file found at {}, but it was missing section named [Default]'.format(str(filepath)))
        return {}


def get_config_path(configuration_tuple):
    client_file = Path(inspect.getfile(configuration_tuple.__class__))
    if hasattr(configuration_tuple, 'cwd'):
        p = Path(configuration_tuple._asdict()['cwd'])
        if not p.absolute():
            p = client_file / p
    else:
        p = client_file
    config_file = find_cfg(p)

    return config_file
