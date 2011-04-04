.. _intro:

概要
====

bpmappersは、Pythonのオブジェクトなどの値を別の辞書へマッピングする操作を支援するモジュールです。

オブジェクトをJSONやXMLへシリアライズする際などに役立ちます。

背景
----

レスポンスをJSONで返すとき、JSONのデータとモデルが一対一にならないことが頻繁にありました。

例を示します。Personモデルを複数所有するTeamモデルがあったとします。TeamモデルのオブジェクトをJSONで返す ``response_json`` 関数を次のように書きました。

.. code-block:: python

   def _map_person(person):
       " personオブジェクトのマッピング "
       return {
           'name': person.fullname,
           'age': person.age,
       }
   
   def _map_team(team):
       " teamオブジェクトのマッピング "
       return {
            'name': team.name,
            'point': team.point,
            'persons': [_map_person(p) for p in team.persons.all()],
       }
   
   def response_json(request):
       team = Team.objects.get(pk=1)  # Djangoのマネージャを使用しています
       return HttpResponse(json.dumps(_map_team(team)))

さて、この時点ではさほど問題はありませんでしたが、後に機能追加、変更によりPersonのnameとTeamのnameのみを返すTeamのJSONが必要になりました。

処理を追加したコードは次のようになりました。

.. code-block:: python

   def _map_person(person):
       " personオブジェクトのマッピング "
       return {
           'name': person.fullname,
           'age': person.age,
       }
   
   def _map_team(team):
       " teamオブジェクトのマッピング "
       return {
            'name': team.name,
            'point': team.point,
            'persons': [_map_person(p) for p in team.persons.all()],
       }
   
   def _map_person_only_name(person):
       " personオブジェクトのマッピング(名前のみ) "
       return {
           'name': person.fullname,
       }
   
   def _map_team_person_name(team):
       " teamオブジェクトのマッピング(名前のみ) "
       return {
            'name': team.name,
            'persons': [_map_person_only_name(p) for p in team.persons.all()],
       }
   
   def response_json(request):
       team = Team.objects.get(pk=1)
       return HttpResponse(json.dumps(_map_team(team)))

   def response_json_name(request):
       team = Team.objects.get(pk=1)
       return HttpResponse(json.dumps(_map_team_person_name(team)))

マッピング用の関数が少し冗長になってきました。似たようなマッピングなのでどうにかしてまとめたいです。

しかし、例えばPersonモデルのマッピングを共通の関数を使用するようにした場合、Teamモデルのマッピングにも変更が必要になります。

このように、マッピングの数や関連が多い場合、変更対してに柔軟に対応するのが難しくなってきて、やがて破綻します。

こうした背景から、 bpmappers を開発しました。

bpmappers を使用すると先ほどのコードは次のようになります。

.. code-block:: python

   class PersonNameMapper(Mapper):
       " personオブジェクトのマッピング(名前のみ) "
       name = RawField('fullname')

   class PersonMapper(PersonNameMapper):
       " personオブジェクトのマッピング "
       age = RawField()

   class TeamPersonNameMapper(Mapper):
       " teamオブジェクトのマッピング(名前のみ) "
       name = RawField()
       persons = ListDelegateField(PersonNameMapper, filter=lambda manager:manager.all())

   class TeamMapper(TeamPersonNameMapper):
       " teamオブジェクトのマッピング "
       point = RawField()
       persons = ListDelegateField(PersonMapper, filter=lambda manager:manager.all())

   def response_json(request):
       team = Team.objects.get(pk=1)
       return HttpResponse(json.dumps(TeamMapper(team).as_dict()))

   def response_json_name(request):
       team = Team.objects.get(pk=1)
       return HttpResponse(json.dumps(TeamPersonNameMapper(team).as_dict()))

似たようなマッピングは、継承を使って定義しています。リスト内包表記は ``ListDelegateField`` で置き換えられています。

また、Mapperクラスにはフックポイントがいくつか用意されているため、後の変更や複雑なマッピングに対しても柔軟に対応できます。

詳しい利用方法は次の :ref:`usage` を参照してください。
