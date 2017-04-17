=========
bpmappers
=========

|build-status| |pypi| |docs|

A mapping tool from model to dictionary.

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

.. |build-status| image:: https://travis-ci.org/beproud/bpmappers.svg?branch=master
   :target: https://travis-ci.org/beproud/bpmappers
.. |docs| image:: https://readthedocs.org/projects/bpmappers/badge/?version=latest
   :target: https://readthedocs.org/projects/bpmappers/
.. |pypi| image:: https://badge.fury.io/py/bpmappers.svg
   :target: http://badge.fury.io/py/bpmappers
