"""
Flamegraph profiler and visualizer for use in IPython notebooks.
See https://github.com/brendangregg/FlameGraph
And https://github.com/23andMe/djdt-flamegraph
"""
from .publons_flame.context_managers import FileFlame


available_contexts = ['FileFlame']

try:
    from .publons_flame.context_managers import InlineFlame
    available_contexts.append('InlineFlame')
except ImportError:
    pass

try:
    from .publons_flame.context_managers import DjangoInlineFlame
    available_contexts.append('DjangoInlineFlame')
except ImportError:
    pass

try:
    from .publons_flame.context_managers import DjangoFileFlame
    available_contexts.append('DjangoFileFlame')
except ImportError:
    pass

__all__ = available_contexts
