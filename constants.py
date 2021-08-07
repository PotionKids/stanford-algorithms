from functools import reduce
from random import randrange
from time import time
from copy import deepcopy
from pprint import pp

MAIN, LINEAR, NL, PLOT = '__main__', lambda x: x, '\n', True

def compose(*fns):
    return reduce(lambda f, g: lambda x: f(g(x)), fns, lambda x: x)
