import subprocess
from xml.sax.saxutils import escape
from pkg_resources import resource_filename


def format_options(options):
    """
    Returns a flattened list of options to pass to a process.
    """
    if 'title' in options:
        options['title'] = escape(options['title'])

    result = []
    for option, value in options.items():
        # Add settings arg to flame if truthy value is present.
        if value:
            result.append('--' + option)

        # only include those values which are actual settings.
        if value and value is not True:
            result.append(str(value))

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

        return ';'.join(str(fn_call) for fn_call in stack) + ' {}'.format(stack_count)

    formatted = '\n'.join([
        format_stack(stack)
        for stack in call_stack_sample.trimmed_stacks()
    ])

    proc = subprocess.Popen(
        args=[resource_filename(__name__, 'flamegraph.pl')] + options,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    out, _ = proc.communicate(formatted)

    return out
