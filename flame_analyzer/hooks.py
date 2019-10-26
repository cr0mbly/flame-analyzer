from datetime import datetime

from humanize import naturaldelta

"""
Hooks allow the flamegraph functionality to be extended in a framework specific
way. By default TimeTakenHook is set but depending on your stack you can further
extend this with a framework specific hook for adding in other functionality
such as DjangoSQLQueriesHook.
"""


class TimeTakenHook:
    """
    Append the time taken to execute to the flame graphs title.
    """
    def before(self):
        self.started = datetime.now()

    def after(self):
        self.time_taken = naturaldelta(datetime.now() - self.started)

    def modify_flame_options(self, flame_options):
        title = flame_options.get('title', '')
        title += 'Excecuted context in {}. '.format(self.time_taken)
        flame_options['title'] = title

        return flame_options


"""
Only add hooks that have the required libaries installed.
"""
try:
    from django import db

    class DjangoSQLQueriesHook:
        """
        Append the number of SQL queries made to the flame graphs title.
        """

        num_sql_queries = 0

        def before(self):
            db.reset_queries()

        def after(self):
            self.num_sql_queries = len(db.connection.queries)

        def modify_flame_options(self, flame_options):
            title = flame_options.get('title', '')
            title += 'Made {} SQL queries. '.format(self.num_sql_queries)
            flame_options['title'] = title

            return flame_options

except ImportError:
    pass
