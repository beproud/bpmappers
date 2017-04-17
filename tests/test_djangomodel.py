from datetime import datetime, date, time

import pytest

from . import testing_django
from .testing import DummyObject

from bpmappers import fields


class TestDjangoFileField:
    @pytest.fixture
    def data(self):
        return DummyObject(url="egg")

    @pytest.fixture
    def target(self):
        from bpmappers.djangomodel import DjangoFileField
        return DjangoFileField()

    def test_url(self, target, data):
        value = target.get_value(None, data)
        assert value == "egg"

    def test_none(self, target):
        value = target.get_value(None, None)
        assert value is None


class TestModelMapper:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            char_field = models.CharField(max_length=30)
            text_field = models.TextField()
            integer_field = models.IntegerField()
            datetime_field = models.DateTimeField()
            date_field = models.DateField()
            time_field = models.TimeField()
            boolean_field = models.BooleanField()

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        return model(
            id=1,
            char_field="egg",
            text_field="ham",
            integer_field=10,
            datetime_field=datetime(2012, 4, 1, 10, 0, 0),
            date_field=date(2012, 4, 1),
            time_field=time(10, 0, 0),
            boolean_field=True)

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'char_field': "egg",
            'text_field': "ham",
            'integer_field': 10,
            'datetime_field': datetime(2012, 4, 1, 10, 0, 0),
            'date_field': date(2012, 4, 1),
            'time_field': time(10, 0, 0),
            'boolean_field': True,
        }
        assert result == expected


class TestMetaFields:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        return model(id=1, spam="egg", bacon="ham")

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class
                fields = ['spam', 'bacon']

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'spam': "egg",
            'bacon': "ham",
        }
        assert result == expected


class TestMetaExclude:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        return model(id=1, spam="egg", bacon="ham")

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class
                exclude = ['id', 'bacon']

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'spam': "egg",
        }
        assert result == expected


class TestAddField:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        return model(id=1, spam="egg", bacon="ham")

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            knight = fields.StubField("ni")

            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'spam': "egg",
            'bacon': "ham",
            'knight': "ni",
        }
        assert result == expected


class TestInheritedModelMapperOverrideField:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        return model(id=1, spam="egg", bacon="ham")

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            spam = fields.StubField("knight")

            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'spam': "knight",
            'bacon': "ham",
        }
        assert result == expected


class TestInheritedModelMapper:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        return model(id=1, spam="egg", bacon="ham")

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        class InheritedMapper(TestMapper):
            class Meta(TestMapper.Meta):
                pass

        return InheritedMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'spam': "egg",
            'bacon': "ham",
        }
        assert result == expected


class TestCustomMapperFields:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        return model(id=1, spam="egg")

    def target(self, model_class):
        from django.db import models
        from bpmappers.djangomodel import ModelMapper

        class CustomMapperField(fields.RawField):
            def as_value(self, mapper, value):
                return "<%s>" % value

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class
                mapper_fields = {
                    models.CharField: CustomMapperField,
                }

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'spam': "<egg>",
        }
        assert result == expected


class TestCreateModelMapper:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    @pytest.fixture
    def target(self):
        from bpmappers.djangomodel import create_model_mapper
        return create_model_mapper

    def test_create_mapper(self, target, model):
        mapper_class = target(model)
        assert len(mapper_class._meta.fields) == 3
        assert 'id' in mapper_class._meta.fields
        assert 'spam' in mapper_class._meta.fields
        assert 'bacon' in mapper_class._meta.fields


class TestForeignKeyFieldModelMapper:
    @pytest.fixture
    def child_model(self):
        from django.db import models

        class ChildModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return ChildModel

    def parent_model(self, child_model):
        from django.db import models

        class ParentModel(models.Model):
            bacon = models.ForeignKey(child_model)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return ParentModel

    def data(self, parent_model, child_model):
        return parent_model(
            id=1,
            bacon=child_model(id=1, spam="egg"))

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, child_model):
        parent_model = self.parent_model(child_model)
        target = self.target(parent_model)
        data = self.data(parent_model, child_model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'bacon': {
                'id': 1,
                'spam': "egg",
            },
        }
        assert result == expected


class TestForeignKeyFieldNullValue:
    @pytest.fixture
    def child_model(self):
        from django.db import models

        class ChildModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return ChildModel

    def parent_model(self, child_model):
        from django.db import models

        class ParentModel(models.Model):
            bacon = models.ForeignKey(child_model, null=True, blank=True)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return ParentModel

    def data(self, parent_model):
        return parent_model(id=1, bacon=None)

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, child_model):
        parent_model = self.parent_model(child_model)
        target = self.target(parent_model)
        data = self.data(parent_model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'bacon': None,
        }
        assert result == expected


class TestForeignKeySelfReference:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.ForeignKey("DummyModel", null=True, blank=True)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        return model(id=1, spam=model(id=2))

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
        }
        assert result == expected


class TestOneToOneFieldModelMapping:
    @pytest.fixture
    def child_model(self):
        from django.db import models

        class ChildModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return ChildModel

    def parent_model(self, child_model):
        from django.db import models

        class ParentModel(models.Model):
            bacon = models.OneToOneField(child_model)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return ParentModel

    def data(self, parent_model, child_model):
        return parent_model(id=1, bacon=child_model(id=1, spam="egg"))

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, child_model):
        parent_model = self.parent_model(child_model)
        target = self.target(parent_model)
        data = self.data(parent_model, child_model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'bacon': {
                'id': 1,
                'spam': "egg",
            },
        }
        assert result == expected


@pytest.mark.django_db
class TestManyToManyFieldModelMapper:
    @pytest.fixture
    def child_model(self):
        from django_app.models import M2M_ChildModel
        return M2M_ChildModel

    @pytest.fixture
    def parent_model(self):
        from django_app.models import M2M_ParentModel
        return M2M_ParentModel

    @pytest.fixture
    def data(self, parent_model, child_model):
        child = child_model(id=1, spam="egg")
        child.save()
        parent = parent_model(id=1)
        parent.save()
        parent.bacon.add(child)
        return parent

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, parent_model, data):
        target = self.target(parent_model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'bacon': [
                {
                    'id': 1,
                    'spam': "egg",
                }
            ],
        }
        assert result == expected


@pytest.mark.django_db
class TestManyToManyFieldThroughModel:
    @pytest.fixture
    def child_model(self):
        from django_app.models import M2M_Through_ChildModel
        return M2M_Through_ChildModel

    @pytest.fixture
    def parent_model(self):
        from django_app.models import M2M_Through_ParentModel
        return M2M_Through_ParentModel

    @pytest.fixture
    def through_model(self):
        from django_app.models import M2M_ThroughModel
        return M2M_ThroughModel

    @pytest.fixture
    def data(self, parent_model, child_model, through_model):
        child = child_model(id=1, spam="egg")
        child.save()
        parent = parent_model(id=1)
        parent.save()
        through = through_model(
            id=1, child=child, parent=parent, knight="ni")
        through.save()
        return through

    @pytest.fixture
    def target(self, through_model):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = through_model

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'knight': "ni",
            'child': {
                'id': 1,
                'spam': "egg",
            },
            'parent': {
                'id': 1,
                'bacon': [{
                    'id': 1,
                    'spam': "egg",
                }],
            },
        }
        assert result == expected




class TestCustomField:
    @pytest.fixture
    def model(self):
        from django.db import models

        class CustomField(models.Field):
            pass

        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        return model(id=1, spam="egg")

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'spam': "egg",
        }
        assert result == expected


class TestFileFieldModelMapper:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.FileField(upload_to='./')

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        obj = model(id=1)
        obj.spam.name = 'egg.txt'
        return obj

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'spam': "egg.txt",
        }
        assert result == expected


class TestImageFieldModelMapper:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.ImageField(upload_to='./')

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def data(self, model):
        obj = model(id=1)
        obj.spam.name = 'egg.jpg'
        return obj

    def target(self, model_class):
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(ModelMapper):
            class Meta:
                model = model_class

        return TestMapper

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'spam': "egg.jpg",
        }
        assert result == expected


class TestMixinModelMapper:
    @pytest.fixture
    def model(self):
        from django.db import models

        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        return DummyModel

    def target(self, model_class):
        from bpmappers.mappers import Mapper
        from bpmappers.djangomodel import ModelMapper

        class TestMapper(Mapper):
            knight = fields.StubField("ni")

        class MixinMapper(TestMapper, ModelMapper):
            class Meta:
                model = model_class

        return MixinMapper

    def data(self, model):
        return model(id=1, spam="egg")

    def test_mapping(self, model):
        data = self.data(model)
        target = self.target(model)
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'id': 1,
            'spam': "egg",
            'knight': "ni",
        }
        assert result == expected
