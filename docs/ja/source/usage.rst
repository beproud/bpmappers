==============
基本的な使い方
==============

マッピングクラスを定義する
==========================

bpmappersを使ってマッピングするためには、まずマッピングクラスを定義します。

マッピングクラスの例を示します:

.. code-block:: python

   from bpmappers import Mapper, RawField
   class SpamMapper(Mapper):
       "マッピングクラス"
       dest_key = RawField('src_key')

マッピングクラスは、 ``bpmappers.Mapper`` を継承して定義します。
``dest_key`` は、マッピング結果の辞書のキー名です。
``src_key`` は、マッピングソースのオブジェクトの属性名、もしくは辞書のキー名です。
マッピングソースから指定した属性名(キー)で取得した値をそのままマッピング結果の値とする場合は ``RawField`` フィールドクラスを使います。

マッピングクラスを使う
======================

定義したマッピングクラスは、次のように使います:

.. code-block:: python

   src_data = {'src_key': 'spam'}  # マッピングソース
   result = SpamMapper(src_data).as_dict()
   # resultは OrderedDict([('dest_key', 'spam')]) となる

マッピングクラスのコンストラクタに、マッピングソースとしてsrc_data変数に代入された辞書を渡しています。
``as_dict()`` メソッドを呼ぶとマッピング処理が実行され、マッピング結果の辞書(OrderedDict)が返されます。

.. note:: バージョン0.9で変更: as_dict()メソッドで返される値は、SortedDictからOrderedDictに変更されました。

入れ子構造のオブジェクトをマッピングする(別のマッピングクラスに委譲する)
========================================================================

親オブジェクトがプロパティで子オブジェクトを持つような、入れ子構造のオブジェクトをマッピングする場合、マッピングクラスのフィールドクラスに ``bpmappers.DelegateField`` を使います。

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
   >>> print(mapper.as_dict())
   OrderedDict([('name', 'python book'), ('author', OrderedDict([('name', 'wozozo')]))])

``bpmappers.DelegateField`` には、引数としてMapperを継承したクラスを指定します。
この例では、マッピングソースの ``Book.author`` は、 ``PersonMapper`` でマッピングされるように定義しています。

入れ子構造のリストをマッピングする
==================================

親子関係のオブジェクトで子がリストになっている場合、 ``bpmappers.ListDelegateField`` を使います。

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
   >>> print(mapper.as_dict())
   OrderedDict([('name', 'php'), ('members', [OrderedDict([('name', 'wozozo')]), OrderedDict([('name', 'moriyoshi')])])])

``bpmappers.ListDelegateField`` には、引数としてMapperを継承したクラスを指定します。
この例では、 ``TeamMapper.members`` の値はリストとして展開されて、 ``PersonMapper`` を使ってマッピングを行うように定義されています。

DjangoのManyToManyFieldをマッピングする場合、ListDelegateFieldにはDjangoのManagerオブジェクトが渡されるため、filterパラメータを指定する必要があります。

.. code-block:: pycon

   >>> from django.db import models
   >>> from bpmappers import Mapper, RawField, ListDelegateField
   >>> class Person(models.Model):
   ...     name = models.CharField(max_length=10)
   ...
   >>> class Group(models.Model):
   ...     name = models.CharField(max_length=10)
   ...     persons = models.ManyToManyField(Person)
   ...
   >>> class PersonMapper(Mapper):
   ...     name = RawField()
   ...
   >>> class GroupMapper(Mapper):
   ...     name = RawField()
   ...     # filterを指定する
   ...     persons = ListDelegateField(PersonMapper, filter=lambda manager: manager.all())
   ...
   >>> person1 = Person.objects.create('wozozo', 123)
   >>> person2 = Person.objects.create('feiz', 456)
   >>> group = Group.objects.create('test')
   >>> group.persons.add(person1)
   >>> group.persons.add(person2)
   >>> mapper = GroupMapper(group)
   >>> print(mapper.as_dict())
   {'name': 'test', [{'name': 'wozozo', 'val': 123}, {'name': 'feiz', 'val': 456}]}

ドット区切りのフィールド指定による参照
======================================

ドット区切りの指定で、深い階層の値を簡単に参照できます。

.. doctest::

   >>> from bpmappers import Mapper, RawField
   >>> class HogeMapper(Mapper):
   ...     hoge = RawField('hoge.piyo.fuga')
   ...
   >>> HogeMapper({'hoge': {'piyo': {'fuga': 123}}}).as_dict()
   OrderedDict([('hoge', 123)])

複数の入力値を1つの値にまとめる
===============================

``Mapper.data`` はインスタンス作成時に引数で与えたものが格納されています。
この例では、入力値としてリストを渡しています。

.. doctest::

   >>> from bpmappers import Mapper, NonKeyField
   >>> class Person(object):
   ...     def __init__(self, name):
   ...         self.name = name
   ...
   >>> class MultiDataSourceMapper(Mapper):
   ...     pair = NonKeyField()
   ...     def filter_pair(self):
   ...         return '%s-%s' % (self.data[0].name, self.data[1].name)
   ...
   >>> MultiDataSourceMapper([Person('foo'), Person('bar')]).as_dict()
   OrderedDict([('pair', 'foo-bar')])
