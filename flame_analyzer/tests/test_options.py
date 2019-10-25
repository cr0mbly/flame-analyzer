from unittest import TestCase
from unittest.mock import patch

from ..context_managers import BaseFlame, DEFAULT_FLAME_WIDTH


class TestOptions(TestCase):

    class TestFlame(BaseFlame):
        def output(self, html):
            pass

    def test_none(self):
        """
        Test nothing is passed when when no options are passed.
        """
        self.assert_generate_flame_graph_html_called_with_options(
            self.TestFlame(),
            ['--width', str(DEFAULT_FLAME_WIDTH)]
        )

    def test_class_options(self):
        """
        Test class options are formatted correctly.
        """
        self.assert_generate_flame_graph_html_called_with_options(
            self.TestFlame(options={'title': 'Default', 'reverse': True}),
            ['--title', 'Default', '--reverse', '--width', str(DEFAULT_FLAME_WIDTH)]
        )

    def test_init_options(self):
        """
        Test init options should override class options.
        """
        self.assert_generate_flame_graph_html_called_with_options(
            self.TestFlame(options={'title': 'Default', 'reverse': None}),
            # Reverse has been removed as it was passed as None.
            ['--title', 'Default', '--width', str(DEFAULT_FLAME_WIDTH)]
        )

    def test_hook_options(self):
        class SetOptionHook:

            def before(self):
                pass

            def after(self):
                pass

            def modify_flame_options(self, flame_options):
                flame_options['title'] += '-Modified'
                flame_options['fontsize'] = 40
                del flame_options['reverse']
                return flame_options

        class TestHookFlame(BaseFlame):

            hook_classes = (SetOptionHook,)

            def output(self, html):
                pass

        self.assert_generate_flame_graph_html_called_with_options(
            TestHookFlame(
                options={'reverse': True, 'fontsize': 20, 'title': 'Test'}
            ),
            [
                '--fontsize', '40', '--title', 'Test-Modified',
                '--width', str(DEFAULT_FLAME_WIDTH)
            ]
        )

    def assert_generate_flame_graph_html_called_with_options(self, instance, options):
        generate_flame_graph_patch = patch(
            'flame_analyzer.context_managers.generate_flame_graph_html'
        )

        with generate_flame_graph_patch as fn:
            instance.__enter__()
            instance.__exit__(None, None, None)
            fn.assert_called_with(instance.sampler.sample, options)
