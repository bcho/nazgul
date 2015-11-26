"""
    nazgul.contrib.multimethod
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Clojure multimethod in python.

    @multimethod
    def dispatch_value(o, *args, **kwargs):
        return o['field']

    @dispatch_value.on('value_a')
    def process_value_a(o, *args, **kwargs):
        pass

    @dispatch_value.on('value_b')
    def process_value_b(o, *args, **kwargs):
        pass

    dispatch_value({'field': 'value_b'}, extra_argument='foo')
"""


class Dispatcher(object):

    def __init__(self, dispatch_func):
        self.dispatch_func = dispatch_func
        self.processors = {}

    def collect(self, value, process_func):
        self.processors[value] = process_func

    def on(self, value):
        def collector(process_func):
            self.collect(value, process_func)
            return process_func
        return collector

    def __call__(self, o, *args, **kwargs):
        dispatch_value = self.dispatch_func(o)
        for value, processor in self.processors.items():
            if dispatch_value == value:
                return processor(o, *args, **kwargs)
        raise RuntimeError(
            'no dispatch func for value `{}`'.format(repr(dispatch_value)))


def multimethod(dispatch_func):
    return Dispatcher(dispatch_func)
