import subprocess
from xml.sax.saxutils import escape
from pkg_resources import resource_filename


def format_options(default_args, default_kwargs, option_args, option_kwargs):
    """
    Combine default args and kwargs with additional options.
    Returns a flattened list of options to pass to a process.
    """
    result = [f'--{x}' for x in option_args] if option_args else default_args

    if option_kwargs:
        default_kwargs.update(option_kwargs)

    # Title is used directly in the SVG and invalid characters cause failures.
    if 'title' in default_kwargs:
        default_kwargs['title'] = escape(default_kwargs['title'])

    for k, v in default_kwargs.items():
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
        universal_newlines=True)
    out, _ = proc.communicate(formatted)

    return out
