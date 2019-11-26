=================
Flame analyzer
=================

.. image:: https://travis-ci.com/publons/flame-analyzer.svg?branch=master
    :target: https://travis-ci.com/publons/flame-analyzer

This package is an often used part of our debug environment at Publons.
It helps benchmark and explain inefficiencies in pieces of code as well as
our dependencies on different service response times.


There are four kinds of Context managers we support with this package

- FileFlame
- InlineFlame
- DjangoFileFlame
- DjangoInlineFlame

They all serve the same use case outputting a Flame graph to your machine for
you to dive into and debug your code. `FileFlame`/`DjangoFileFlame` save the
graph to an SVG for you to share, while `InlineFlame`/`DjangoInlineFlame` will
render it in your IPython browser.

Examples
--------

Saving a Flame graph to an SVG can be done with the following benchmarking

.. code-block:: python

    from flame_analyzer import FileFlame


    with FileFlame('./file_flame_test.svg'):
        # Some expensive piece of code.
        [len(u.email) for u in  User.objects.all()]

Or directly to the IPython notebook

.. code-block:: python

    from flame_analyzer import InlineFlame


    with InlineFlame():
        # Some expensive piece of code.
        [len(u.email) for u in  User.objects.all()]

You can also optionally configure the width by adding the width kwarg

.. code-block:: python

    with FileFlame(
        './file_flame_test.svg', flame_width=1200,
        options={'title': 'This is my test title'}
    ):
        # some expensive piece of code
        [len(u.email) for u in  User.objects.all()]


Extensions
----------

By default both IPython and Django are optional imports meaning you can install
this library and use it in the terminal to debug your app code without them
installed. Support can be added for other Database frameworks or if your
wanting to hook into the context enter/exit methods by creating your own hooks
and adding to the output flame type your wanting for example

.. code-block:: python

    from flame_analyzer import InlineFlame

    class CustomHook:
        """
        Append the time taken to execute to the flame graphs title.
        """
        def before(self):
            self.called_before = '< Called before code execution >'

        def after(self):
            self.called_after = '< Called after code execution >'

        def modify_flame_options(self, flame_options):
            title = flame_options.get('title', '')
            flame_options['title'] = self.called_before + ' --- ' + self.called_after
            return flame_options


    class CustomInlineFlame(InlineFlame):
        hook_classes = (CustomHook,)

    with CustomInlineFlame(flame_width=500):
        total_email_length = 0
        for u in User.objects.all():
            total_email_length += len(u.email)
        print(total_email_length)


Outputs the IPython viewed Graph

.. image:: https://user-images.githubusercontent.com/6813352/68050764-c1107800-fd4a-11e9-94a2-8ab0bc564617.png

Credits to the following projects:
 - https://github.com/brendangregg/FlameGraph
 - https://github.com/23andMe/djdt-flamegraph
