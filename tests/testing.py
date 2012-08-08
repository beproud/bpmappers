from unittest2 import TestCase


class DummyCallback(object):
    "Utility class for callback test."
    def __init__(self, returns=None):
        self.returns = returns
        self.called = False

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.called = True
        return self.returns
