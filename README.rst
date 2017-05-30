=========
bpmappers
=========

|build-status| |pypi| |docs|

bpmappers is a Python moudle that maps Python dictionary values and object properties to different dictionary.

Install
=======

Install using pip.

::

   $ pip install bpmappers

Usage
=====

An example of mapping an instance of the Person class to a dictionary:

.. doctest::

   >>> class Person:
   ...     def __init__(self, name, age):
   ...         self.name = name
   ...         self.age = age
   ...     def __repr__(self):
   ...         return "<Person name={}, age={}>".format(self.name, self.age)
   ...
   >>> p = Person("Spam", 25)
   >>> p
   <Person name=Spam, age=25>
   >>> from bpmappers import Mapper, RawField
   >>> class PersonMapper(Mapper):
   ...     mapped_name = RawField('name')
   ...     mapped_age = RawField('age')
   ...
   >>> PersonMapper(p).as_dict()
   OrderedDict([('mapped_name', 'Spam'), ('mapped_age', 25)])

Requirements
============

- Target Python version is 2.7, 3.4, 3.5, 3.6
- Django>=1.8 (If use Django support)

License
=======

This software is licensed under the MIT License.

Documentation
=============

The latest documentation is hosted at Read The Docs.

https://bpmappers.readthedocs.io/en/latest/

Develop
=======

This project is hosted at Github: https://github.com/beproud/bpmappers

Author
======

- BeProud, Inc

Maintainer
==========

- Shinya Okano <tokibito@gmail.com>

.. |build-status| image:: https://travis-ci.org/beproud/bpmappers.svg?branch=master
   :target: https://travis-ci.org/beproud/bpmappers
.. |docs| image:: https://readthedocs.org/projects/bpmappers/badge/?version=latest
   :target: https://readthedocs.org/projects/bpmappers/
.. |pypi| image:: https://badge.fury.io/py/bpmappers.svg
   :target: http://badge.fury.io/py/bpmappers
