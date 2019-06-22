from configz import c, replace_signatures
from fire import Fire


class Cli:
    def foo(self, **ps):
        """docstring wtf"""
        print(c(ps))

    def dir(self, test, testx=None):
        print(Cli.dir.__get__)


def main():
    replace_signatures(Cli)
    Fire(Cli)


if __name__ == '__main__':
    main()
