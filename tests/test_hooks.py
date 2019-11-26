from time import sleep
from unittest import TestCase
from unittest.mock import patch

from flame_analyzer.hooks import DjangoSQLQueriesHook, TimeTakenHook


class TestTimeTakeHook(TestCase):

    hook = TimeTakenHook()

    def test_time_is_tracked(self):
        self.hook.before()
        sleep(1)
        self.hook.after()

        modified_options = self.hook.modify_flame_options({})
        self.assertEqual(
            'Excecuted context in {}. '.format(self.hook.time_taken),
            modified_options['title'],
        )


class TestDjangoSQLQueriesHook(TestCase):

    hook = DjangoSQLQueriesHook()

    def test_db_queries_are_tracked(self):
        num_sql_queries = 2

        with patch(
            'flame_analyzer.hooks.'
            'DjangoSQLQueriesHook.num_sql_queries',
            num_sql_queries
        ):
            modified_options = self.hook.modify_flame_options({})

        self.assertEqual(
            'Made {} SQL queries. '.format(num_sql_queries),
            modified_options['title']
        )
