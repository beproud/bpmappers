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

    def __repr__(self):
        return "<%s returns=%s called=%s>" % (
            self.__class__.__name__, self.returns, self.called)


class DummyObject(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
