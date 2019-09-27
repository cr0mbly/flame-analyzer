"""
Flamegraph profiler and visualizer for use in IPython notebooks.
See https://github.com/brendangregg/FlameGraph
And https://github.com/23andMe/djdt-flamegraph
"""

from .context_managers import FileFlame, InlineFlame

__all__ = ['FileFlame', 'InlineFlame']
