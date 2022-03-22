リリース手順
==============

事前準備
--------------

* TestPyPIのアカウントを取得し、bpmappersの編集権限を付与してもらう
* PyPIのアカウントを取得し、bpmappersの編集権限を付与してもらう
* GitHubアカウントに、bpmappersの編集権限を付与してもらう
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

4. TestPyPIでdescriptionが正しく表示されていること、ビルドしたパッケージがアップロードされていることを確認する
5. もしTestPyPIでのアップロードが失敗していた場合、下記の「備考」を参考にパッケージのバージョンを変更して再度アップロードする
6. ローカル環境にて、pipでTestPyPIにアップロードしたパッケージがインストール可能であることを確認する

   * ``pip install -i https://test.pypi.org/simple/ bpmappers==1.3`` (「1.3」の部分は確認したいバージョン番号に変更)
   * ``pip freeze | grep bpmappers``

7. GitHubで次バージョンのReleaseタグを作成して、Publish Releaseする
8. もしTestPyPIでの確認用にパッケージ名を変更している場合、本番アップロード用のパッケージを再ビルドする

   * ``python setup.py sdist bdist_wheel``

9. PyPIにアップロードする

   * ``python -m twine upload dist/*``

備考
======

TestPyPIに同じバージョンで、再アップロードしたい時
--------------------------------------------------

TestPyPIとPyPIでは、同じバージョンのパッケージを再度アップロードすることができません。

そのため、TestPyPIでメタ情報のアップロードに失敗した場合は、本番環境のバージョン番号に影響を与えないように、postN(Post-release segment)のバージョン番号を変更して再度アップロードします。

次の postNの部分を、post1, post2, post3 ...などと変更して、異なるバージョンのパッケージを作成します。

* ``python setup.py egg_info --tag-build=postN sdist bdist_wheel``



