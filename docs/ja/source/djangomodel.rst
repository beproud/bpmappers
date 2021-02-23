.. _djangomodel:

============================================
Djangoフレームワークのモデルをマッピングする
============================================

Djangoフレームワークのモデルインスタンスをマッピングする場合、 ``bpmappers.djangomodel.ModelMapper`` を使用することができます。

Djangoフレームワークのバージョン
================================

READMEに記載されているDjangoのバージョンをサポートしています。

ModelMapperの使用
=================

ModelMapperを使用するには、 ModelMapper を継承したクラスを定義します。

Djangoで次のようなモデルを定義したとします:

.. code-block:: python

   from django.db import models

   class Person(models.Model):
       name = models.CharField(max_length=10)

   class Book(models.Model):
       title = models.CharField(max_length=10)
       author = models.ForeignKey(Person)

ModelMapperを使ってBookモデルを辞書にマッピングするための定義は次のようになります:

.. code-block:: python

   from bpmappers.djangomodel import ModelMapper
   from myapp.models import Book

   class BookMapper(ModelMapper):
       class Meta:
           model = Book

ModelMapperを使わない場合は次のようになります:

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
======

ModelMapperは、Djangoモデルクラスのメタ情報(``Model._meta.fields``)を参照してマッピング定義を作成しています。

Djangoのモデルフィールドとbpmppersのフィールドの対応は次の通りです:

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
==================

``ModelMapper`` を継承したクラスには、 ``Meta`` インナークラスを定義する必要があります。このクラスで定義した内容から、マッピングルールが生成されます。

Meta.model
----------

Djangoのモデルクラスを指定します。

Meta.fields
-----------

``Meta.model`` で指定したモデルクラスのフィールドのうち、マッピング対象とするフィールド名をシーケンス型で列挙します。省略した場合はすべてのフィールドがマッピング対象になります。

Meta.exclude
------------
``Meta.model`` で指定したモデルクラスのフィールドのうち、マッピング対象から除外するフィールド名をシーケンス型で列挙します。省略した場合は、すべてのフィールドがマッピング対象になります。
