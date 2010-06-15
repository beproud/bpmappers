.. _usage:

======
使い方
======

シンプルなマッピング
====================

シンプルなオブジェクトのマッピング例を以下に示します。

.. code-block:: pycon

  >>> from bpmappers import Mapper, RawField
  >>> class Person(object):
  ...     def __init__(self, name, value):
  ...         self.name = name
  ...         self.value = value
  ...
  >>> class PersonMapper(Mapper):
  ...     username = RawField('name')
  ...     num = RawField('value')
  ...
  >>> obj = Person('wozozo', 123)
  >>> mapper = PersonMapper(obj)
  >>> print mapper.as_dict()
  {'username': 'wozozo', 'num': 123}

この例では、Personクラスのオブジェクトの要素を辞書にマッピングしています。

Djangoモデルからマッパークラスを作成する
========================================

Djangoのモデルをマッピングする際には、マッパークラスを簡単に作成することができます。

.. code-block:: pycon

  >>> from django.db import models
  >>> from bpmappers.djangomodel import *
  >>> class Person(models.Model):
  ...    name = models.CharField(max_length=10)
  ...    val = models.IntegerField()
  ...
  >>> class PersonMapper(ModelMapper):
  ...     class Meta:
  ...         model = Person
  ...
  >>> obj = Person('wozozo', 123)
  >>> mapper = PersonMapper(obj)
  >>> print mapper.as_dict()
  {'name': 'wozozo', 'val': 123}

