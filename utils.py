from datetime import timedelta
import math
import os
import subprocess
from xml.sax.saxutils import escape

from django.conf import settings

MILLISECONDS_IN_SECOND = 1000
SECONDS_IN_DAY = 86400
SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = SECONDS_IN_MINUTE * SECONDS_IN_MINUTE
HOURS_IN_DAY = 24


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
        args=[os.path.join(settings.ROOT, 'flame', 'flamegraph.pl'), *options],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True)
    out, _ = proc.communicate(formatted)

    return out



def humanize_timedelta(td, precision='s', lower=None, upper=None):
    """
    Format a number of seconds into a nicer time string.
    """

    if upper and td > upper:
        td = upper

    if lower and td < lower:
        td = lower

    seconds = td.seconds + (SECONDS_IN_DAY * td.days)
    seconds = math.floor(seconds)

    # Format
    d = seconds // SECONDS_IN_DAY
    h = seconds // SECONDS_IN_HOUR % HOURS_IN_DAY
    m = seconds // SECONDS_IN_MINUTE % SECONDS_IN_MINUTE
    s = seconds % SECONDS_IN_MINUTE
    ms = td.microseconds // MILLISECONDS_IN_SECOND

    parts = []

    if d > 0 and precision in ('d', 'h', 'm', 's', 'ms'):
        plural = 'days' if d > 1 else 'day'
        parts.append(f"{d} {plural}")

    if h > 0 and precision in ('h', 'm', 's', 'ms'):
        plural = 'hours' if h > 1 else 'hour'
        parts.append(f"{h} {plural}")

    if m > 0 and precision in ('m', 's', 'ms'):
        plural = 'minutes' if m > 1 else 'minute'
        parts.append(f"{m} {plural}")

    if s > 0 and precision in ('s', 'ms'):
        plural = 'seconds' if s > 1 else 'second'
        parts.append(f"{s} {plural}")

    if ms > 0 and precision == 'ms':
        plural = 'milliseconds' if ms > 1 else 'millisecond'
        parts.append(f"{ms} {plural}")

    if not parts:

        if precision == 'd':
            return "< 1 day"
        if precision == 'h':
            return "< 1 hour"
        if precision == 'm':
            return "< 1 minute"
        if precision == 's':
            return "< 1 second"
        if precision == 'ms':
            return "< 1 ms"

    return oxford_comma(parts)


def oxford_comma(values, and_or='and'):
    """
    Format a list of values into a grammatically correct comma separated string.
    """
    values = list(map(str, values))

    if len(values) == 0:
        return ''

    if len(values) == 1:
        return values[0]

    if len(values) == 2:
        return f' {and_or} '.join(values)

    return ', '.join(values[:-1]) + f', {and_or} ' + values[-1]
