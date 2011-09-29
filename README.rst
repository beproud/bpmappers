=========
bpmappers
=========

Model to dictionary mapping for Python.

::

   >>> from bpmappers import Mapper, RawField
   >>> class SpamMapper(Mapper):
   ...     spam = RawField('foo')
   ...     egg = RawField('bar')
   ...
   >>>
   >>> SpamMapper(dict(foo=123, bar='abc')).as_dict()
   {'egg': 'abc', 'spam': 123}
   >>>
   >>> class FooModel(object):
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   >>> SpamMapper(FooModel(foo=123, bar='abc')).as_dict()
   {'egg': 'abc', 'spam': 123}
   >>>
   >>> class HogeMapper(Mapper):
   ...     hoge = RawField('hoge.piyo.fuga')
   ...
   >>> HogeMapper({'hoge': {'piyo': {'fuga': 123}}}).as_dict()
   {'hoge': 123}
