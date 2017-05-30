==============
フックポイント
==============

マッピング処理の途中で何か追加の処理を行いたい場合、いくつかのフックポイントを使用できます。

Mapper.filter_FOO
=================

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
=======================

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
=================

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
==============

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
====================

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
===============

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
