from configz import c
from fire import Fire


class Cli:
    def __init__(self, **ps):
        c(**ps)
        print(f'configured c: {repr(c())}')

    def foo(self):
        """docstring wtf"""
        print(c().b)


def main():
    Fire(Cli)
