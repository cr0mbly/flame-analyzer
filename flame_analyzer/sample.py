import copy
import signal


class Sampler:
    """
    Sample the stack.
    """
    def __init__(self, interval):
        self.sample = CallStackSample()
        self.interval = interval

    def start(self):
        signal.signal(signal.SIGALRM, self._sample_call_stack)
        signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)

    def stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0, 0)

    def _sample_call_stack(self, signum, frame):
        stack = []
        while frame is not None:
            stack.append(
                FunctionCall(
                    name=frame.f_code.co_name,
                    path=frame.f_globals.get('__name__'),
                )
            )
            frame = frame.f_back

        self.sample.add_stack(stack[::-1])


class CallStackSample:
    """
    Stores a collection of function call stacks.
    """
    def __init__(self):
        self.stacks = []
        self.common_fn_calls = []

    def add_stack(self, stack):
        self.stacks.append(stack)
        self.measure_common_fn_calls(stack)

    def trimmed_stacks(self):
        """
        Return stacks filtering out elements common to the root of all stacks.
        """
        return [
            stack[self.highest_common_fn_call_index():]
            for stack in self.stacks
        ]

    def highest_common_fn_call_index(self):
        return len(self.common_fn_calls)

    def measure_common_fn_calls(self, new_stack):
        # First iteration, nothing to compare.
        if not self.common_fn_calls:
            self.common_fn_calls = copy.deepcopy(new_stack)
            return

        # Cut the common stack to the depth of the shortest stack, there
        # can't be common function calls where one stack is deeper than the
        # other.
        min_stack_depth = min(len(new_stack), len(self.common_fn_calls))
        self.common_fn_calls = self.common_fn_calls[:min_stack_depth]

        # Compare each existing function call in the common stack with its
        # match in the new stack to find the deepest common function call.
        common_stack_depth = 0
        for a, b in zip(self.common_fn_calls, new_stack):
            if a == b:
                common_stack_depth += 1

        # Throw away non common function calls.
        self.common_fn_calls = self.common_fn_calls[:common_stack_depth]


class FunctionCall:
    """
    Data container for a function call in the stack.
    """
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __eq__(self, other):
        if isinstance(other, FunctionCall):
            return self.name == other.name and self.path == other.path
        return False

    def __str__(self):
        return '{}({})'.format(self.name, self.path)

    def __repr__(self):
        return str(self)
