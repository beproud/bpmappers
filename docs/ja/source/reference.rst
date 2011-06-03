.. _reference:

============
リファレンス
============

class Mapper
============

.. class:: Mapper(data=None, \*\*options)

:data: マッピング元のオブジェクト(デフォルト値: None).
:\*\*options: オプション引数(デフォルト値: なし)

.. method:: Mapper.as_dict()

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

.. method:: Mapper.order(parsed)

:parsed: 変換済みのフィールド名-値の辞書

as_dictメソッドの最後に呼ばれます。順序付き辞書のソート順を変更する場合にオーバーライドします。

.. method:: Mapper.key_name(name, value, field)

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

.. class:: NonKeyField([callback=None, after_callback=None, \*args, \*\*kwargs])

マッピング対象のdataにキーがない場合に使用します。

class StubField
===============

.. class:: StubField([stub={}, \*args, \*\*kwargs])

stubで指定した固定値を返すフィールドです。

class Field
===========

.. class:: Field([key=None, callback=None, \*args, \*\*kwargs])

キーを持つフィールドのクラス。通常は継承して使用します。

class RawField
==============

.. class:: RawField([key=None, callback=None, \*args, \*\*kwargs])

マッピング対象のdataに対してキーで取得した内容をそのまま返すフィールドです。

class ChoiceField
=================

.. class:: ChoiceField(choices, [key=None, callback=None, \*args, \*\*kwargs])

class DelegateField
===================

.. class:: DelegateField(mapper_class, [key=None, callback=None, before_filter=None, required=True, attach_parent=False, \*args, \*\*kwargs])

.. method:: DelegateField.before_filiter(value)

class NonKeyDelegateField
=========================

.. class:: NonKeyDelegateField(mapper_class, [callback=None, filter=None, required=True, attach_parent=False, \*args, \*\*kwargs])

class ListDelegateField
=======================

.. class:: ListDelegateField(mapper_class, [key=None, callback=None, filter=None, after_filter=None, \*args, \*\*kwargs])

.. method:: ListDelegateField.filter(value)

.. method:: ListDelegateField.after_filter(value)

class NonKeyListDelegateField
=============================

.. class:: NonKeyListDelegateField(mapper_class, [callback=None, \*args, \*\*kwargs])

.. method:: NonKeyListDelegateField.filter(value=None)

