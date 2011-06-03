.. _djangomodel:

Djangoフレームワークのモデルをマッピングする
============================================

Djangoフレームワークのモデルインスタンスをマッピングする場合、 ``bpmappers.djangomodel.ModelMapper`` を使用することができます。

Djangoフレームワークのバージョン
--------------------------------

``bpmappers.djangomodel`` は、Djangoフレームワークのバージョンが 1.0 から 1.3 に対応しています。

1.0 以前のバージョンへの対応予定は、今のところありません。

ModelMapperの使用
-----------------

ModelMapperを使用するには、 ModelMapper を継承したクラスを定義します。

次のようなモデルを定義したとします:

.. code-block:: python

   from django.db import models

   class Person(models.Model):
       name = models.CharField(max_length=10)

   class Book(models.Model):
       title = models.CharField(max_length=10)
       author = models.Foreignkey(Person)

ModelMapper を使ってBookモデルを辞書にマッピングするための定義は次のようになります:

.. code-block:: python

   from bpmappers.djangomodel import ModelMapper
   from myapp.models import Book

   class BookMapper(ModelMapper):
       class Meta:
           model = Book

ModelMapper を使わない場合は次のようになります:

.. code-block:: python

   from bpmappers import Mapper, RawField, DelegateField

   class PersonMapper(Mapper):
       id = RawField()
       name = RawField()

   class BookMapper(Mapper):
       id = RawField()
       title = RawField()
       author = DelegateField(PersonMapper)

仕組み
------

ModelMapper は、Djangoモデルクラスの ``Model._meta.fields`` のモデルフィールドの定義を参照してマッピングフィールドを作成しています。

モデルフィールドとマッピングフィールドの対応は次の通りです:

========================  ==========================================
Djangoのモデルフィールド  bpmappersのフィールド
========================  ==========================================
AutoField                 bpmappers.RawField
CharField                 bpmappers.RawField
TextField                 bpmappers.RawField
IntegerField              bpmappers.RawField
DateTimeField             bpmappers.RawField
DateField                 bpmappers.RawField
TimeField                 bpmappers.RawField
BooleanField              bpmappers.RawField
FileField                 bpmappers.djangomodel.DjangoFileField
ForeignKey                bpmappers.DelegateField
ManyToManyField           bpmappers.ListDelegateField
========================  ==========================================

Metaインナークラス
------------------

``ModelMapper`` を継承したクラスには、 ``Meta`` インナークラスを定義する必要があります。このクラスで定義した内容から、マッピングルールが生成されます。

Meta.model
~~~~~~~~~~

Djangoのモデルクラスを指定します。

Meta.fields
~~~~~~~~~~~

``Meta.model`` で指定したモデルクラスのフィールドのうち、マッピング対象とするフィールド名をシーケンス型で列挙します。省略した場合はすべてのフィールドがマッピング対象になります。

Meta.exclude
~~~~~~~~~~~~
``Meta.model`` で指定したモデルクラスのフィールドのうち、マッピング対象から除外するフィールド名をシーケンス型で列挙します。省略した場合は、すべてのフィールドがマッピング対象になります。
