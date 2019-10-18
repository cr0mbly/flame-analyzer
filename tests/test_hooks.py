from time import sleep
from unittest import TestCase
from unittest.mock import patch

from ..publons_flame.hooks import TimeTakenHook


class TestTimeTakeHook(TestCase):

    hook = TimeTakenHook()

    def test_time_is_tracked(self):
        self.hook.before()
        sleep(1)
        self.hook.after()

        modified_options = self.hook.modify_flame_options({})
        self.assertEqual(
            'Excecuted context in a second.',
            modified_options['title'],
        )


try:
    from ..publons_flame.hooks import DjangoSQLQueriesHook

    class TestDjangoSQLQueriesHook(TestCase):

        hook = DjangoSQLQueriesHook()

        def test_db_queries_are_tracked(self):
            num_sql_queries = 2

            with patch(
                'publons_flame.publons_flame.hooks.'
                'DjangoSQLQueriesHook.num_sql_queries',
                num_sql_queries
            ):
                modified_options = self.hook.modify_flame_options({})

            self.assertEqual(
                f'Made {num_sql_queries} SQL queries.',
                modified_options['title']
            )

except ImportError:
    pass
