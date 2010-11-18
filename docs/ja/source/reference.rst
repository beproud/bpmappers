.. _reference:

============
リファレンス
============

class Mapper
============

__init__
~~~~~~~~

:data: マッピング元のオブジェクト(デフォルト値: None).
:\*\*options: オプション引数(デフォルト値: なし)

as_dict
~~~~~~~~

引数なし。マッピングした辞書を返します。

filter_FOO
~~~~~~~~~~

引数なし。FOOにはフィールド名を指定します。

filter_FOOメソッドは、オブジェクトから取り出してデータを評価したあとに実行されます。

after_filter_FOO
~~~~~~~~~~~~~~~~

class ModelMapper
=================

__init__
~~~~~~~~

Mapperクラスと同様です。

as_dict
~~~~~~~

Mapperクラスと同様です。

class NonKeyField
=================

class Field
===========

class RawField
==============

class ChoiceField
=================

class DelegateField
===================

class ListDelegateField
=======================

class NonKeyListDelegateField
=============================

