from unittest import TestCase
from unittest.mock import patch

import sys
sys.path.append("..")

from ..context_managers import BaseFlame



class TestOptions(TestCase):

    def test_none(self):
        """
        Test nothing is passed when when no options are passed.
        """
        class NoOutputFlame(BaseFlame):
            def output(self, html):
                pass

        self.assert_generate_flame_graph_html_called_with_options(
            NoOutputFlame(),
            []
        )

    def test_class_options(self):
        """
        Test class options are formatted correctly.
        """
        class NoOutputFlame(BaseFlame):
            def get_defaults(self):
                return {'title': 'Default', 'reverse': ''}

            def output(self, html):
                pass

        self.assert_generate_flame_graph_html_called_with_options(
            NoOutputFlame(),
            ['--reverse', '--title', 'Default']
        )

    def test_init_options(self):
        """
        Test init options should override class options.
        """
        class NoOutputFlame(BaseFlame):
            def get_defaults(self):
                return {'title': 'Default', 'reverse': None}

            def output(self, html):
                pass

        self.assert_generate_flame_graph_html_called_with_options(
            NoOutputFlame(
                {'title': 'Default'}
            )
            # Reverse has been removed as it was passed as None.
            ['--title', 'Test']
        )

    def test_hook_options(self):
        class SetOptionHook:

            def before(self):
                pass

            def after(self):
                pass

            def modify_flame_options(self, options):
                options['title'] += '-Modified'
                options['fontsize'] = 20
                del options['reverse']

        class NoOutputFlame(BaseFlame):

            hook_classes = [SetOptionHook]

            def get_defaults(self):
                return ['reverse'], {'title': 'Default'}

            def output(self, html):
                pass

        self.assert_generate_flame_graph_html_called_with_options(
            NoOutputFlame(),
            ['--title', 'Test-Modified', '--fontsize', '20']
        )


    def assert_generate_flame_graph_html_called_with_options(self, instance, options):
        sampler_patch = patch('publons_flame.context_managers.Sampler')
        generate_flame_graph_patch = patch(
            'publons_flame.context_managers.generate_flame_graph_html'
        )

        with generate_flame_graph_patch as fn:
            instance.__enter__()
            instance.__exit__(None, None, None)
            fn.assert_called_with(instance.sampler.sample, options)
