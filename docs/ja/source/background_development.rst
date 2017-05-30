==========
開発の背景
==========

WebAPIのレスポンスをJSONやXMLなどの構造化テキストで返すとき、アプリケーションのデータ構造とAPIのインターフェースの構造は一致しないことが頻繁にありました。

例えば、次のような構造のJSONを返すWebAPIの仕様があったとします(フォーラムのコメントデータ):

.. code-block:: json

   {
     "comment_id": 1,
     "content": "This is a comment.",
     "posted_by": {
       "user_id": 2,
       "name": "Sato",
       "age": 40
     }
   }

このデータは、アプリケーション上では次のようなデータ構造で保持されていることがあります:

.. code-block:: python3

   class User:
       def __init__(self, id: int, name: str, age: int):
           self.id = id
           self.name = name
           self.age = age

   class Comment:
       def __init__(self, id: int, content: str, posted_by: User):
           self.id = id
           self.content = content
           self.posted_by = posted_by

   user = User(1, "Sato", 40)
   comment = Comment(1, "This is a comment.", user)

WebAPIの仕様に従ったJSONと等価の辞書を生成する場合、次のようなコードを書くかもしれません:

.. code-block:: python

   data = {
     'comment_id': comment.id,
     'content': comment.content,
     'posted_by': {
       'user_id': comment.posted_by.id,
       'name': comment.posted_by.name,
       'age': comment.posted_by.age
     }
   }

posted_byの内容を返す部分を再利用したくなった場合、関数に分けるかもしれません:

.. code-block:: python3

   def map_user(user: User):
       return {
           'user_id': user.id,
           'name': user.name,
           'age': user.age
       }

   data = {
     'comment_id': comment.id,
     'content': comment.content,
     'posted_by': map_user(comment.posted_by)
   }

このように再利用の単位で関数を作っていくと、似たような機能の関数がいくつも作られてしまうことがありました。また、リストをマッピングする場合はforループも使うことになり、マッピングのコードは見通しが悪くなってきます。

こうした背景から、bpmappersを開発しました。

bpmappersではマッピングルールを宣言的に書くことでき、コードはスッキリします。

bpmappersを使うとこのように書けます:

.. code-block:: python

   from bpmappers import Mapper, RawField, DelegateField
   class UserMapper(Mapper):
       user_id = RawField('id')
       name = RawField()
       age = RawField()

   class CommentMapper(Mapper):
       comment_id = RawField('id')
       content = RawField()
       posted_by = DelegateField(UserMapper)

   data = CommentMapper(comment).as_dict()

他にもマッピング処理のフックポイントや、DjangoフレームワークのORM向けのサポートを含んでいます。

bpmappersを利用することで、あなたのデータマッピングのコードがスッキリすることを願っています。
