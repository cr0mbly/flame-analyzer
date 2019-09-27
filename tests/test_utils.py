from datetime import timedelta
from unittest import TestCase

from ..utils import humanize_timedelta, oxford_comma


class TestHumanizeTimedelta(TestCase):


    test_values = (
        (
            {
                'td': timedelta(minutes=5),
                'lower': timedelta(minutes=2),
                'upper': timedelta(minutes=4),
            },
            '4 minutes',
        ),
        (
            {
                'td': timedelta(minutes=1),
                'lower': timedelta(minutes=2),
                'upper': timedelta(minutes=4),
            },
            '2 minutes',
        ),
        (
            {
                'td': timedelta(minutes=3),
                'lower': timedelta(minutes=2),
                'upper': timedelta(minutes=4),
            },
            '3 minutes',
        ),
        (
            {'td': timedelta(minutes=5)},
            '5 minutes',
        ),
        (
            {
                'td': timedelta(minutes=3),
                'precision': 'd',
            },
            '< 1 day',
        ),
        (
            {
                'td': timedelta(minutes=10, seconds=10),
                'precision': 'm',
            },
            '10 minutes',
        ),
        (
            {
                'td': timedelta(minutes=10, seconds=20, milliseconds=400),
                'precision': 'ms',
            },
            '10 minutes, 20 seconds, and 400 milliseconds'
        ),
        (
            {
                'td': timedelta(minutes=10),
                'precision': 'ms',
            },
            '10 minutes',
        ),
        (
            {'td': timedelta(milliseconds=10)},
            '< 1 second',
        ),
        (
            {
                'td': timedelta(milliseconds=20),
                'precision': 'ms',
            },
            '20 milliseconds',
        ),
    )

    def test_humanize_time(self):
        for kwargs, expected_output in self.test_values:
            self.assertEqual(expected_output, humanize_timedelta(**kwargs))


class TestOxfordComma(TestCase):

    test_values = (
        (([],), ''),
        (([1],), '1'),
        (([1, 2],), '1 and 2'),
        (([1, 2, 3],), '1, 2, and 3'),
        (([1, 2, 3,4],), '1, 2, 3, and 4'),
        (([1, 2, 3,4], 'or'), '1, 2, 3, or 4'),
    )

    def test_oxford_comma(self):
        for args, expected_output in self.test_values:
            self.assertEqual(expected_output, oxford_comma(*args))
