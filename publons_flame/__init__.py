"""
Flamegraph profiler and visualizer for use in IPython notebooks.
See https://github.com/brendangregg/FlameGraph
And https://github.com/23andMe/djdt-flamegraph
"""
import sys

from .import context_managers
from .import tests

# from .context_managers import FileFlame, InlineFlame
# from .tests import *
# __all__ = ['FileFlame', 'InlineFlame']


import unittest

if __name__ == '__main__':
    unittest.main()
