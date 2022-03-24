リリース手順
==============

事前準備
--------------

* GitHub, PyPI, TestPyPIのアカウントにbpmappersの編集権限を設定
* パッケージのビルドに使用するパッケージをインストール

  * ``pip install wheel twine``


手順
--------------------
1. 次バージョンのパッケージをビルド

   * ``python setup.py sdist bdist_wheel``

2. twineのコマンドを実行して、エラーが出ないことを確認

   * ``twine check --strict dist/*``

3. dist/に作成したパッケージをTestPyPIへアップロード

   * ``twine upload --repository testpypi dist/*``

4. TestPyPIで、descriptionがエラーなく表示されていることと、ビルドしたパッケージがアップロードされていることを確認

   * TestPyPIへアップロードした内容に問題がある場合、修正したパッケージをTestPyPIに再度アップロード

5. GitHubで次バージョンのReleaseタグを作成し、Publish Releaseを実行

   * dist/に試行錯誤したパッケージが残っている場合、一度全て削除し、本番アップロード用のパッケージを再度作成

6. dist/に作成したパッケージを本番環境のPyPIにアップロード

   * ``twine upload dist/*``
