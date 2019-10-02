# Publons Flame

This package is an often used part of our debug environment at Publons.
It helps benchmark and explain inefficiencies is pieces of code,
you might find that this helps you too!


There's two kinds of Context managers we support with this application

- FileFlame
- InlineFlame

They both serve the same use case outputting a Flame graph to your
machine for you to dive into and debug your code. `FileFlame` save's
it as an SVG for you to share, while `InlineFlame` will render it in
your IPython browser.


### Examples


Saving a Flame graph to an SVG can be done with the following benchmarking code

```Python
    from publons_flame import FileFlame


    with FileFlame('./file_flame_test.svg'):
        # Some expensive piece of code.
        [len(u.email) for u in  User.objects.all()]
```

Or directly to the IPython notebook

```Python
    from publons_flame import InlineFlame


    with InlineFlame():
        # Some expensive piece of code.
        [len(u.email) for u in  User.objects.all()]
```


You can also optionally configure the width by adding the width kwarg

```Python
    with FileFlame('./file_flame_test.svg', option_kwargs={'width': 1000}):
        # some expensive piece of code
```

### Extensions

By default both IPython and Django are optional imports meaning you can install this libarary and use it in the terminal without InlineFlame. Support can be added for other Database frameworks or if your wanting to hook into the context enter/exit methods by creating your own mixin and adding to the output flame type your wanting for example:

```Python

from publons_flame.context_managers import InlineFlame
from pulbons_flame.hooks import BaseHookMixin

class MyCustomHookMixin(BaseHookMixin):

    def enter_section_hook(self):
        # Code to be run on enter of context manager
        pass
        
    def exit_section_hook(self, default_kwargs):
        # Code to be run on exit of context manager
        pass
class MyCustomFlame(MyCustomHookMixin, InlineFlame)
    pass
    
    
with MyCustomFlame():
    # do expensive work and output to IPython
    pass
```

Credits to the following projects:
 - https://github.com/brendangregg/FlameGraph
 - https://github.com/23andMe/djdt-flamegraph
