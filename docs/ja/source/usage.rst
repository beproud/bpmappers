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
   # resultは {'dest_key': 'spam'} となる

マッピングクラスのコンストラクタに、マッピングソースとしてsrc_data変数に代入された辞書を渡しています。
``as_dict()`` メソッドを呼ぶとマッピング処理が実行され、マッピング結果の辞書が返されます。

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

.. note:: この機能はバージョン0.5で追加されました。

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


フックポイント
==============

マッピング処理の途中で何か追加の処理を行いたい場合、いくつかのフックポイントを使用できます。

Mapper.filter_FOO
-----------------

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
   OrderedDict([('value', 10)])

Mapper.after_filter_FOO
-----------------------

フィールドの値変換の後に実行されます。FOOはフィールド名に置き換えてください。
第一引数に、filter_FOOの結果の値が入ります。

.. doctest::

   >>> from bpmappers import Mapper, NonKeyField
   >>> class MyMapper(Mapper):
   ...     value = NonKeyField()
   ...     def filter_value(self):
   ...         return "oyoyo"
   ...     
   ...     def after_filter_value(self, val):
   ...         return val.capitalize()
   ... 
   >>> mapper = MyMapper()
   >>> print(mapper.as_dict())
   OrderedDict([('value', 'Oyoyo')])


Mapper.attach_FOO
-----------------

マッピングの結果の辞書に値を追加する代わりに実行されます。値を追加しない場合や、値の追加位置を変更する場合などに使用できます。

.. doctest::

   >>> from bpmappers import Mapper, NonKeyField, RawField
   >>> class Point(object):
   ...     def __init__(self, x, y):
   ...         self.x = x
   ...         self.y = y
   ... 
   >>> class PointMapper(Mapper):
   ...     x = RawField("x")
   ...     y = RawField("y")
   ...
   ...     def attach_x(self, parsed, v):
   ...         parsed[v] = (v, v*v, v*v*v, v*v*v*v)
   ...
   ...     def attach_y(self, parsed, v):
   ...         parsed[v] = "y is %s" % v
   ... 
   >>> mapper = PointMapper(Point(10, 20))
   >>> print(mapper.as_dict())
   OrderedDict([(10, (10, 100, 1000, 10000)), (20, 'y is 20')])

Field.callback
--------------

フィールドの値変換の前に実行されます。 ``filter_FOO`` の後にフィールドクラスで実行されます。

.. doctest::

   >>> from bpmappers import Mapper, RawField, DelegateField
   >>> class Person(object):
   ...     def __init__(self, name):
   ...        self.name = name
   ... 
   >>> class PersonInfoMapper(Mapper):
   ...     info = RawField("name", callback = lambda v : "name:%s" % v)
   ... 
   >>> 
   >>> class PersonInfoMapper2(Mapper):
   ...     info = RawField("name", callback = lambda v : "name:%s" % v)
   ...     
   ...     def filter_info(self, v):
   ...         return v+v
   ... 
   >>> mapper = PersonInfoMapper(Person("bucho"))
   >>> print(mapper.as_dict())
   OrderedDict([('info', 'name:bucho')])
   >>> mapper = PersonInfoMapper2(Person("bucho"))
   >>> print(mapper.as_dict())
   OrderedDict([('info', 'name:buchobucho')])

Field.after_callback
--------------------

フィールドの値変換の後に実行されます。 ``after_filter_FOO`` の前にフィールドクラスで実行されます。

.. doctest::

   >>> from bpmappers import Mapper, RawField, ListDelegateField
   >>> class Person(object):
   ...     def __init__(self, name):
   ...         self.name = name
   ... 
   >>> class Book(object):
   ...     def __init__(self, title, authors):
   ...         self.title = title
   ...         self.authors = authors
   ... 
   >>> class AuthorMapper(Mapper):
   ...     author = RawField("name")
   ... 
   >>> class BookMapper(Mapper):
   ...     title = RawField()
   ...     authors = ListDelegateField(AuthorMapper)
   ... 
   >>> book = Book("be clound", [Person("bucho"), Person("shacho")])
   >>> print(BookMapper(book).as_dict())
   OrderedDict([('title', 'be clound'), ('authors', [OrderedDict([('author', 'bucho')]), OrderedDict([('author', 'shacho')])])])
   >>> def get_vals(items):
   ...     """
   ...     辞書のリストから、値だけを取り出す関数
   ... 
   ...     >>> get_vals([{"pt":1}, {"pt":2}])
   ...     [1, 2]
   ...     """
   ...     result = []
   ...     for dic in items:
   ...         for k, v in dic.items():
   ...             result.append(v)
   ...     return result
   ... 
   >>> class BookMapperExt(Mapper):
   ...     title = RawField()
   ...     authors = ListDelegateField(AuthorMapper, after_callback=get_vals)
   ... 
   >>> book = Book("be clound", [Person("bucho"), Person("shacho")])
   >>> print(BookMapperExt(book).as_dict())
   OrderedDict([('title', 'be clound'), ('authors', ['bucho', 'shacho'])])


.. note::
   filter_FOO, after_filter_FOO, callback, after_callbackは以下の順序で呼ばれます。

   #. filter_FOO
   #. callback
   #. after_callback
   #. after_filter_FOO

   実行例

   .. doctest::

      >>> from bpmappers import Mapper, RawField, DelegateField
      >>> class Person(object):
      ...     def __init__(self, name):
      ...         self.name = name
      ... 
      >>> class PersonInfoMapper(Mapper):
      ...     info = RawField("name",
      ...                     callback= lambda v :  "( cb: %s )" % v, 
      ...                     after_callback = lambda v :  "[ after_cb: %s ]" % v)
      ...
      ...     def filter_info(self, v): 
      ...         return "< filter: %s >" % v
      ...
      ...     def after_filter_info(self, v): 
      ...         return "{ after_filter: %s }" % v
      ... 
      >>> mapper = PersonInfoMapper(Person("BP"))
      >>> print(mapper.as_dict())
      OrderedDict([('info', '{ after_filter: [ after_cb: ( cb: < filter: BP > ) ] }')])


Mapper.key_name
---------------

キー名を変更したい場合などに使用します。

.. doctest::

   >>> from bpmappers import Mapper, RawField
   >>> class NameSpaceMapper(Mapper):
   ...     name = RawField()
   ...     def key_name(self, name,  value, field):
   ...         return 'namespace:%s' % name
   ...
   >>> NameSpaceMapper(dict(name='bucho')).as_dict()
   OrderedDict([('namespace:name', 'bucho')])
