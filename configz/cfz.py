from configz import c, prepare_signatures
from fire import Fire


class Cli:
    def __init__(self, **ps):
        c(ps)

    def foo(self):
        """docstring wtf"""
        print('foo')
        print(c())

    def bar(self):
        print('bar')
        print(Cli.dir.__get__)


def main():
    prepare_signatures(Cli)
    Fire(Cli)


if __name__ == '__main__':
    main()
