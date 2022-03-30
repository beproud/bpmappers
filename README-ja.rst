=========
bpmappers
=========

|build-status| |pypi| |docs|

bpmappersは、Pythonの辞書の値やオブジェクトのプロパティを別の辞書へマッピングするPythonモジュールです。

インストール
============

pip を使ってインストールします。

::

   $ pip install bpmappers

使い方
======

Personクラスのインスタンスを辞書に変換する例です:

.. code-block:: pycon

   >>> class Person:
   ...     def __init__(self, name, age):
   ...         self.name = name
   ...         self.age = age
   ...     def __repr__(self):
   ...         return "<Person name={}, age={}>".format(self.name, self.age)
   ...
   >>> p = Person("Spam", 25)
   >>> p
   <Person name=Spam, age=25>
   >>> from bpmappers import Mapper, RawField
   >>> class PersonMapper(Mapper):
   ...     mapped_name = RawField('name')
   ...     mapped_age = RawField('age')
   ...
   >>> PersonMapper(p).as_dict()
   OrderedDict([('mapped_name', 'Spam'), ('mapped_age', 25)])

動作要件
========

- Pythonのバージョン 3.6, 3.7, 3.8, 3.9
- Django 2.2, 3.0, 3.1 (Djangoサポートを使用する場合)

ライセンス
==========

MITライセンス

ドキュメント
============

最新のドキュメントはReadTheDocsでホストされています。

https://bpmappers.readthedocs.io/ja/latest/

開発
====

* このプロジェクトはGitHubでホストされています: https://github.com/beproud/bpmappers
* リリース手順: https://github.com/beproud/bpmappers/blob/master/release_checklist.rst

作者
====

- BeProud, Inc

メンテナ
========

- Shinya Okano <tokibito@gmail.com>

.. |build-status| image:: https://github.com/beproud/bpmappers/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/beproud/bpmappers/actions
.. |docs| image:: https://readthedocs.org/projects/bpmappers/badge/?version=latest
   :target: https://bpmappers.readthedocs.io/ja/latest/
.. |pypi| image:: https://badge.fury.io/py/bpmappers.svg
   :target: http://badge.fury.io/py/bpmappers
