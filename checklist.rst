リリース手順
==============

事前準備
--------------

* TestPyPIのアカウントを取得する
* PyPIのアカウントを取得する
* Githubアカウントに、bpmappersの編集権限を付与してもらう
* パッケージのビルドに使用するパッケージをインストールする

  * ``pip install wheel twine``


手順
--------------------
1. 次バージョンのパッケージをビルドする

   * ``python setup.py sdist bdist_wheel``

2. twineのコマンドを実行して、PyPIでパッケージのドキュメントを正しく表示できそうか確認する

   * ``twine check --strict dist/*``

3. TestPyPIにアップロードする

   * ``python -m twine upload --repository testpypi dist/*``

4. TestPyPIの表示を確認する
5. もしTestPyPIでの表示が正しくない場合、下記の「備考」を参考にパッケージのバージョンを変更して再度アップロードする
6. ローカル環境にて、pipでTestPyPIにアップロードしたパッケージがインストール可能であることを確認する

   * ``pip install Django~=2.2 Celery~=4.1 six``
   * ``pip install -i https://test.pypi.org/simple/ bpmappers``
   * ``pip freeze | grep bpmappers``

7. Githubで次バージョンのRelaseタグを作成して、Publish Releaseする
8. もしTestPyPIでの確認用にパッケージ名を変更している場合、本番アップロード用のパッケージを再ビルドする。

   * ``python setup.py sdist bdist_wheel``

9. PyPIにアップロードする

   * ``python -m twine upload dist/*``

備考
======

TestPyPIに同じバージョンで、再アップロードしたい時
--------------------------------------------------

postN(Post-release segment)のバージョン番号を変更して再度アップロードする

次の postNの部分を、post1, post2, post3 ...などと変更する

* ``python setup.py egg_info --tag-build=postN sdist bdist_wheel``



