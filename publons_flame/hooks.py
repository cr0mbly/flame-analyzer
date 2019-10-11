from datetime import datetime

from humanize import naturaldelta

class TimeTaken:
    """
    Append the time taken to execute to the flame graphs title.
    """
    def before(self):
        self.started = datetime.now()

    def after(self):
        self.time_taken = naturaldelta(datetime.now() - self.started)
        return default_kwargs

    def modify_flame_options(self, args, kwargs):
        title = kwargs.get('title', '')
        title += f'Excecuted context in {self.time_taken}.'
        kwargs['title'] = title

try:
    from django import db
    class DjangoSQLHookMixin:
        """
        Append the number of SQL queries made to the flame graphs title.
        """
        def before(self):
            db.reset_queries()

        def after(self, default_kwargs):
            self.num_sql_queries = len(db.connection.queries)

        def modify_flame_options(self, args, kwargs):
            title = kwargs.get('title', '')
            title += f'Made {num_sql_queries} SQL queries.'
            title['title'] = title

except ImportError:
    pass  # Django not installed.
