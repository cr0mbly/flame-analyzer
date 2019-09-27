from abc import abstractmethod, ABC
import copy
from datetime import datetime

from django import db
from IPython.core import display

from .sample import Sampler
from .utils import (
    format_options,
    generate_flame_graph_html,
    humanize_timedelta,
)

FLAME_FILE_WIDTH = 1904
FLAME_IPYTHON_WIDTH = 1904
SAMPLE_INTERVAL = 0.001


class BaseFlame(ABC):
    """
    Base context manager to sample a block of code.
    """
    def __init__(
        self, *, interval=SAMPLE_INTERVAL, option_args=None, option_kwargs=None
    ):
        self.sampler = Sampler(interval)
        self.option_args = copy.deepcopy(option_args)
        self.option_kwargs = copy.deepcopy(option_kwargs)

    def __enter__(self):
        """
        On Context enter reset sampler and db queries to
        track functional and db calls.
        """
        self.sampler.start()
        self.started = datetime.now()
        db.reset_queries()

    def __exit__(self, type, value, traceback):
        """
        On Context completion dump the summed functional calls for display.
        """
        self.sampler.stop()  # Always stop the sampler.
        time_taken = humanize_timedelta(
            datetime.now() - self.started, precision='ms'
        )

        num_sql_queries = len(db.connection.queries)

        default_args, default_kwargs = self.get_defaults()
        default_kwargs['title'] = (
            f'Made {num_sql_queries} SQL queries in {time_taken}.'
        )

        options = format_options(
            default_args, default_kwargs, self.option_args, self.option_kwargs
        )

        # Only generate Flamegraph if we generated the sample successfully.
        if not traceback:
            html = generate_flame_graph_html(self.sampler.sample, options)
            self.output(html)

    @abstractmethod
    def output(self, *args, **kwargs):
        pass

    def get_defaults(self):
        return [], {}


class FileFlame(BaseFlame):
    """
    Write an HTML / SVG at a given path.
    """
    def __init__(self, path, **kwargs):
        self.path = path
        super().__init__(**kwargs)

    def get_defaults(self):
        return [], {'width': FLAME_FILE_WIDTH}

    def output(self, data):
        with open(self.path, 'w') as f:
            f.write(data)


class InlineFlame(BaseFlame):
    """
    Render FlameGraph HTML / SVG in an IPythonNotebook.
    """
    def get_defaults(self):
        return [], {'width': FLAME_IPYTHON_WIDTH}

    def output(self, data):
        return display.display(display.SVG(data=data))
