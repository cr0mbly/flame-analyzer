from time import sleep
from unittest import TestCase

from ..context_managers import SAMPLE_INTERVAL
from ..sample import Sampler, FunctionCall

class TestFunctionCallSampler(TestCase):

    def test_sampler_returns_most_common_call(self):
        # Given a attempted stack sample
        sampler = Sampler(SAMPLE_INTERVAL)

        # When we sample a period of execution
        sampler.start()
        expensive_method_call()
        sampler.stop()

        # Then include the expensive calls in the sampler call stack
        common_calls = sampler.sample.common_fn_calls
        self.assertIn(
            FunctionCall(
                name=expensive_method_call.__name__,
                path=expensive_method_call.__module__,
            ),
            common_calls
        )

def expensive_method_call():
    """
    Mock function for testing expensive functional calls
    """
    for x in range(100):
        y = [v for v in range(x)]
        sleep(0.0001)
