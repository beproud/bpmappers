.. _flatten:

同じ階層にマッピング結果をマージする
====================================

``myapp/models.py`` に定義した次のようなPersonモデルとBookモデルを同じ階層にマッピングする例です。


.. code-block:: python

   from django.db import models

   class Person(models.Model):
       name = models.CharField(max_length=20)
       age = models.PositiveIntegerField()

       def __unicode__(self):
           return '%s, %d' % (self.name, self.age)

   class Book(models.Model):
       title = models.CharField(max_length=30)
       author = models.ForeignKey(Person)

       def __unicode__(self):
           return '%s, %s' % (self.title, self.author)


``myapp/mappers.py`` にマッピングルールを定義します。
``DelegateField`` の ``attach_parent`` オプションに ``True`` を指定することで、対象のマッピング結果を同じ階層のマッピング結果にマージします。

.. code-block:: python

   from bpmappers import Mapper, fields, djangomodel
   from myapp.models import Person, Book

   class PersonModelMapper(djangomodel.ModelMapper):
       class Meta:
           model = Person
           exclude = ['id']

   class BookFlattenMapper(djangomodel.ModelMapper):
       author = fields.DelegateField(PersonModelMapper, attach_parent=True)

       class Meta:
           model = Book


結果はこのようになります:

.. code-block:: pycon

   >>> from myapp.models import Book
   >>> book = Book.objects.get(pk=1)
   >>> book
   <Book: feizbook, feiz, 23>
   >>> from myapp.mappers import BookFlattenMapper
   >>> BookFlattenMapper(book).as_dict()
   {'name': u'feiz', 'age': 23, 'id': 1, 'title': u'feizbook'}

