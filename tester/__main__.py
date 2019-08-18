from typing import NamedTuple
from clinfig import prepare, c


class Configuration(NamedTuple):
    a: str = 'A'  # a description
    x: int = 1  # x description


# Hack to enable autocompletion in IDEs
c: Configuration = c


class Cli:
    def __init__(self, **cli_args):
        c(cli_args, Configuration())

    def subcommand_foo(self):
        """This will be shown in --help for subcommand-foo"""
        print('foo')
        print(c.a)
        print(c.x)

    def subcommand_bar(self):
        """This will be shown in --help for subcommand-bar"""
        print('bar')
        print(repr(c))


def main():
    prepare(Cli, Configuration())


if __name__ == '__main__':
    main()
