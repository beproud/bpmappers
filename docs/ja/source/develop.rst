.. _develop:

====
開発
====

開発版リポジトリ
================

開発版のソースコードは `Mercurial <http://mercurial.selenic.com/>`_ で管理され、Bitbucket上でホストされています。

:Bitbukect上のページ: https://bitbucket.org/tokibito/python-bpmappers/

開発版リポジトリをローカルマシンにcloneするには、以下のようにシェル上でコマンドを実行します。

::

   $ hg clone https://bitbucket.org/tokibito/python-bpmappers/

テストの実行
============

テストは `tox <http://pypi.python.org/pypi/tox>`_ で実行します。

::

   $ cd python-bpmappers
   $ tox

各Python環境はUbuntuであれば `deadsnakes PPA <https://launchpad.net/~fkrull/+archive/deadsnakes>`_ を使用すると簡単に用意できます。

CI
==

Travis CI上でtoxを実行しています。

.. image:: https://travis-ci.org/tokibito/bpmappers.png?branch=master

:URL: https://travis-ci.org/tokibito/bpmappers
