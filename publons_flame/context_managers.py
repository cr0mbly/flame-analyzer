from abc import abstractmethod, ABC
import copy

from .sample import Sampler
from .utils import (
    format_options,
    generate_flame_graph_html,
)

DEFAULT_FLAME_WIDTH = 1904
SAMPLE_INTERVAL = 0.001


class BaseFlame(ABC):
    """
    Base context manager to sample a block of code.
    """
    def __init__(self, *, interval=SAMPLE_INTERVAL, options=None):
        self.sampler = Sampler(interval)
        self.option = copy.deepcopy(options)
        self.hooks = [
            hook() for hook in self.get_hook_classes()
        ]

    def __enter__(self):
        """
        On Context enter reset sampler and db queries to
        track functional and db calls.
        """
        self.sampler.start()
        for hook in self.hooks:
            hook.before()

    def __exit__(self, type, value, traceback):
        """
        On Context completion dump the summed functional calls for display.
        """
        self.sampler.stop()  # Always stop the sampler.

        options = self.get_defaults()
        options.update(self.options)

        for hook in self.hooks[::-1]:
            hook.after()
            hook.modify_flame_options(options)

        # Only generate Flamegraph if we generated the sample successfully.
        if not traceback:
            html = generate_flame_graph_html(
                self.sampler.sample,
                format_options(options)
            )
            self.output(html)

    @abstractmethod
    def output(self, html):
        pass

    def get_defaults(self):
        return {}

    def get_hook_classes(self):
        return getattr(self, 'hook_classes', [])


class FileFlame(BaseFlame):
    """
    Write an HTML / SVG at a given path.
    """
    def __init__(self, path, **kwargs):
        self.path = path
        super().__init__(**kwargs)

    def get_defaults(self):
        return [], {'width': DEFAULT_FLAME_WIDTH}

    def output(self, html):
        with open(self.path, 'w') as f:
            f.write(html)

##
# Support Ipython only if library is installed
##


try:
    from IPython.core import display

    class InlineFlame(BaseFlame):
        """
        Render FlameGraph HTML / SVG in an IPythonNotebook.
        """
        def get_defaults(self):
            return [], {'width': DEFAULT_FLAME_WIDTH}

        def output(self, html):
            return display.display(display.SVG(data=data))

except ImportError:
    pass
