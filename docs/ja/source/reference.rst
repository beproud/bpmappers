.. _reference:

============
リファレンス
============

.. automodule:: bpmappers

class Mapper
============

.. autoclass:: Mapper
   :members:

:data: マッピング元のオブジェクト(デフォルト値: None).
:\*\*options: オプション引数(デフォルト値: なし)

.. automethod:: Mapper.as_dict

マッピングした順序付き辞書(SortedDict)を返します。

.. method:: Mapper.filter_FOO(value)

FOOにはフィールド名を指定します。

オブジェクトから取り出してデータを評価したあとに実行されます。

フィールドが NonKeyField の場合、引数なしで呼び出されます。

.. method:: Mapper.after_filter_FOO(value)

FOOにはフィールド名を指定します。

Field.get_value のあとに実行されます。

.. method:: Mapper.attach_FOO(parsed, value)

:parsed: 変換済みのフィールド名-値の辞書
:value: 変換済みの値

FOOにはフィールド名を指定します。

このメソッドを記述した場合、マッピング結果の辞書への値の追加は自前の処理で行う必要があります。

.. automethod:: Mapper.order

:parsed: 変換済みのフィールド名-値の辞書

as_dictメソッドの最後に呼ばれます。順序付き辞書のソート順を変更する場合にオーバーライドします。

.. automethod:: Mapper.key_name

:name: マッピング先の辞書のキー名
:value: 変換済みの値
:field: 処理中のFieldオブジェクト

as_dictメソッドから呼ばれます。マッピング先のキー名をマッピングの直前に変換したい場合に使います。

class ModelMapper
=================

.. class:: ModelMapper(data=None, \*\*options)

Djangoモデルクラスからマッピング定義を生成します。

class NonKeyField
=================

.. autoclass:: NonKeyField

マッピング対象のdataにキーがない場合に使用します。

class StubField
===============

.. autoclass:: StubField

stubで指定した固定値を返すフィールドです。

class Field
===========

.. autoclass:: Field

キーを持つフィールドのクラス。通常は継承して使用します。

class RawField
==============

.. autoclass:: RawField

マッピング対象のdataに対してキーで取得した内容をそのまま返すフィールドです。

class ChoiceField
=================

.. autoclass:: ChoiceField

class DelegateField
===================

.. autoclass:: DelegateField

.. automethod:: DelegateField.before_filter

class NonKeyDelegateField
=========================

.. autoclass:: NonKeyDelegateField

class ListDelegateField
=======================

.. autoclass:: ListDelegateField

.. automethod:: ListDelegateField.filter

.. automethod:: ListDelegateField.after_filter

class NonKeyListDelegateField
=============================

.. autoclass:: NonKeyListDelegateField

.. automethod:: NonKeyListDelegateField.filter
