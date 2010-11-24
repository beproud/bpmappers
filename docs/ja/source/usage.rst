.. _usage:

使い方
======

シンプルなマッピング
--------------------

シンプルなオブジェクトのマッピング例を以下に示します。

.. doctest::

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
`bpmappers.Mapper` クラスを継承して、各フィールドに対応するマッピングをクラス属性に定義します。

Djangoモデルからマッパークラスを作成する
----------------------------------------

Djangoのモデルをマッピングする場合、ヘルパーを使ってマッピングを簡単に作成することができます。
``bpmappers.djangomodel.ModelMapper`` を使用した例を示します。

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

別のマッパーへの委譲
--------------------

特定のフィールドのマッピングを別のマッパークラスに委譲するには、 ``DelegateField`` を使用します。

.. doctest::

   >>> from bpmappers import  Mapper, RawField, DelegateField
   >>> class Person(object):
   ...     def __init__(self, name):
   ...         self.name = name
   ...
   >>> class Book(object):
   ...     def __init__(self, name, author):
   ...         self.name = name
   ...         self.author = author
   ...
   >>> class PersonMapper(Mapper):
   ...     name = RawField()
   ...
   >>> class BookMapper(Mapper):
   ...     name = RawField()
   ...     author = DelegateField(PersonMapper)
   ...
   >>> p = Person('wozozo')
   >>> b = Book('python book', p)
   >>> mapper = BookMapper(b)
   >>> print mapper.as_dict()
   {'name': 'python book', 'author': {'name': 'wozozo'}}

リストのマッピング
~~~~~~~~~~~~~~~~~~

リストなどのシーケンスをマッピングを委譲するには、 ``ListDelegateField`` を使用します。

.. doctest::

   >>> from bpmappers import  Mapper, RawField, ListDelegateField
   >>> class Person(object):
   ...     def __init__(self, name):
   ...         self.name = name
   ...
   >>> class Team(object):
   ...     def __init__(self, name, members):
   ...         self.name = name
   ...         self.members = members
   ...
   >>> class TeamMapper(Mapper):
   ...     name = RawField()
   ...     members = ListDelegateField(PersonMapper)
   ...
   >>> p1 = Person('wozozo')
   >>> p2 = Person('moriyoshi')
   >>> t = Team('php', [p1, p2])
   >>> mapper = TeamMapper(t)
   >>> print mapper.as_dict()
   {'name': 'php', 'members': [{'name': 'wozozo'}, {'name': 'moriyoshi'}]}

フックポイント
--------------

マッピング処理の途中で何か独自の処理を行いたい場合、いくつかのフックポイントを使用できます。

Mapper.filter_FOO
~~~~~~~~~~~~~~~~~

フィールドの値変換の前に実行されます。FOOはフィールド名に置き換えてください。

``NonKeyField`` を使った場合、ここでマッピングに利用する値を生成することができます。

.. doctest::

   >>> from bpmappers import Mapper, NonKeyField
   >>> class MyMapper(Mapper):
   ...     value = NonKeyField()
   ...     def filter_value(self):
   ...         return 10
   ...
   >>> mapper = MyMapper()
   >>> mapper.as_dict()
   {'value': 10}

Mapper.after_filter_FOO
~~~~~~~~~~~~~~~~~~~~~~~

フィールドの値変換の後に実行されます。FOOはフィールド名に置き換えてください。

Mapper.attach_FOO
~~~~~~~~~~~~~~~~~

マッピングの結果の辞書に値を追加する前に実行されます。値を追加しない場合や、値の追加位置を変更する場合などに使用できます。

Field.callback
~~~~~~~~~~~~~~

フィールドの値変換の前に実行されます。 ``filter_FOO`` の後にフィールドクラスで実行されます。

Field.after_callback
~~~~~~~~~~~~~~~~~~~~

フィールドの値変換の後に実行されます。 ``after_filter_FOO`` の前にフィールドクラスで実行されます。
