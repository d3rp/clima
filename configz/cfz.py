from typing import NamedTuple
from configz import prepare, c


class Configuration(NamedTuple):
    a: str = 'a'  # a description
    b: str = 'b'  # b description
    x: int = 1  # x description
    y: int = 0  # y description


class Cli:
    def __init__(self, **ps):
        print('init')
        c(ps, Configuration())

    def foo(self):
        """docstring wtf"""
        print('foo')
        print(c())

    def bar(self):
        """Docstring ftw"""
        print('bar')
        print(Cli.dir.__get__)


def main():
    prepare(Cli, Configuration())


if __name__ == '__main__':
    main()
