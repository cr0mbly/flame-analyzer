=================
Publons Flame
=================

This package is an often used part of our debug environment at Publons.
It helps benchmark and explain long inefficiencies is pieces of code,
you might find that this helps you too!


There's two kinds of Context managers we support with this application

- FileFlame
- InlineFlame

They both serve the same use case outputting a Flame graph to your
machine for you to dive into and debug your code. `FileFlame` save's
it as an SVG for you to share, while `InlineFlame` will render it in
your IPython browser.


Examples
--------

    from publons_flame import FileFlame


    with FileFlame('./file_flame_test.svg'):
        # Some expensive piece of code.

        [len(u.email) for u in  User.objects.all()]


.. image::  https://raw.github.com/pulbons/publons-flame/master/docs/_static/file_flame_test.svg


You can also optionally configure the width by adding the kwarg

    with FileFlame('./file_flame_test.svg', option_kwargs={'width': 1000})

Where 1000 is the number of pixels.
