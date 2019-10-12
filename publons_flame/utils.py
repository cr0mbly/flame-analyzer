import subprocess
from xml.sax.saxutils import escape
from pkg_resources import resource_filename


def format_options(options):
    """
    Returns a flattened list of options to pass to a process.
    """
    options = {k: v for k, v in options.items() if v}

    if 'title' in options:
        options['title'] = escape(options['title'])

    result = []
    for k, v in options.items():
        result.append('--' + k)
        result.append(str(v))

    return result


def generate_flame_graph_html(call_stack_sample, options):
    """
    Generate HTML from a call stack sample by running it through Flamegraph.pl.
    """
    def format_stack(stack):
        # It is possible to group identical stacks together when passing input
        # to flamegraph.pl. I've taken the simple approached and not aggregated
        # identical stacks together.
        stack_count = 1

        return ';'.join(str(fn_call) for fn_call in stack) + f' {stack_count}'

    formatted = '\n'.join([
        format_stack(stack)
        for stack in call_stack_sample.trimmed_stacks()
    ])

    proc = subprocess.Popen(
        args=[resource_filename('publons_flame', 'flamegraph.pl'), *options],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    out, _ = proc.communicate(formatted)

    return out
