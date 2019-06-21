from configz import C, c, configure
from fire import Fire

from pprint import pformat

class Cli:
    def __init__(self, **ps):
        configure(**ps)
        self.c = c()

    def foo(self, **params):
        """docstring wtf"""
        print(c().b)

    def bar(self, x=None):
        print('oh hi')

    def baz(self):
        pformat(C._field_defaults)



def main():
    Fire(Cli)
