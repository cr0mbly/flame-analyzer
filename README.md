# Flame analyzer

This package is an often used part of our debug environment at Publons.
It helps benchmark and explain inefficiencies is pieces of code,
you might find that this helps you too!


There's four kinds of Context managers we support with this application

- FileFlame
- InlineFlame
- DjangoFileFlame
- DjangoInlineFlame

They all serve the same use case outputting a Flame graph to your
machine for you to dive into and debug your code. `FileFlame`/`DjangoFileFlame` save the graph
to an SVG for you to share, while `InlineFlame`/`DjangoInlineFlame` will render it in
your IPython browser.


### Examples


Saving a Flame graph to an SVG can be done with the following benchmarking code

```Python
    from flame_analyzer import FileFlame


    with FileFlame('./file_flame_test.svg'):
        # Some expensive piece of code.
        [len(u.email) for u in  User.objects.all()]
```

Or directly to the IPython notebook

```Python
    from flame_analyzer import InlineFlame


    with InlineFlame():
        # Some expensive piece of code.
        [len(u.email) for u in  User.objects.all()]
```


You can also optionally configure the width by adding the width kwarg

```Python
    with FileFlame('./file_flame_test.svg', options={'title': 'This is my test title'}):
        # some expensive piece of code
```

### Extensions

By default both IPython and Django are optional imports meaning you can install this libarary and use it in the terminal without InlineFlame. Support can be added for other Database frameworks or if your wanting to hook into the context enter/exit methods by creating your own hooks and adding to the output flame type your wanting for example:

```Python

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
```

![image](https://user-images.githubusercontent.com/6813352/67134922-471fbf80-f271-11e9-9ed7-b31354af6ab2.png)

Credits to the following projects:
 - https://github.com/brendangregg/FlameGraph
 - https://github.com/23andMe/djdt-flamegraph
