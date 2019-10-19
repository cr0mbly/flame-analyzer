from abc import abstractmethod, ABC
import copy

from .hooks import TimeTakenHook
from .sample import Sampler
from .utils import generate_flame_graph_html, format_options

DEFAULT_FLAME_WIDTH = 1904
SAMPLE_INTERVAL = 0.001


class BaseFlame(ABC):
    """
    Base context manager to sample a block of code.
    """
    def __init__(
        self, interval=SAMPLE_INTERVAL, flame_width=DEFAULT_FLAME_WIDTH, options=None,
    ):
        self.sampler = Sampler(interval)
        self.options = copy.deepcopy(options) if options is not None else {}
        self.options['width'] = flame_width

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

        for hook in self.hooks[::-1]:
            hook.after()
            hook.modify_flame_options(self.options)

        # Only generate Flamegraph if we generated the sample successfully.
        if not traceback:
            html = generate_flame_graph_html(
                self.sampler.sample,
                format_options(self.options),
            )
            self.output(html)

    @abstractmethod
    def output(self, html):
        pass

    def get_hook_classes(self):
        return getattr(self, 'hook_classes', [])


class FileFlame(BaseFlame):
    """
    Write an HTML / SVG at a given path.
    """

    hook_classes = (TimeTakenHook,)

    def __init__(self, path, **kwargs):
        self.path = path
        super().__init__(**kwargs)

    def output(self, html):
        with open(self.path, 'w') as f:
            f.write(html)

##
# Implementations supported in base flame_analyzer, availability dependent on
# implementers installed libraries. Out of the box flame_analyzer supports
# - FileFlame (File saved base implementation)
# - InlineFlame (IPython base implementation)
# - DjangoInlineFlame (Django tuned Ipython implementation)
# - DjangoFileFlame (Django tuned file stored implementation)
##


try:
    from .hooks import DjangoSQLQueriesHook
    django_hook = DjangoSQLQueriesHook
except ImportError:
    django_hook = None


try:
    from IPython.core import display
    ipython_display = display
except ImportError:
    ipython_display = None


if ipython_display:
    class InlineFlame(BaseFlame):
        """
        Render FlameGraph HTML / SVG in an IPythonNotebook.
        """
        hook_classes = (TimeTakenHook,)

        def output(self, html):
            return ipython_display.display(ipython_display.SVG(data=html))


if django_hook:
    class DjangoFileFlame(FileFlame):
        hook_classes = (TimeTakenHook, django_hook)

if ipython_display and django_hook:
    class DjangoInlineFlame(InlineFlame):
        hook_classes = (TimeTakenHook, django_hook)
