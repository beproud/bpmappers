from datetime import datetime, date, time

import testing_django

from testing import TestCase, SkipTest

from bpmappers import fields
from bpmappers import mappers

models = None
djangomodel = None


def setUpModule():
    if not testing_django.LIB_ENABLED_DJANGO:
        raise SkipTest("Django is not installed.")
    testing_django.initialize()
    # replace models
    global models
    from django.db import models as django_models
    models = django_models
    # replace djangomodel
    global djangomodel
    from bpmappers import djangomodel as bpmappers_djangomodel
    djangomodel = bpmappers_djangomodel


class ModelMapperTest(TestCase):
    def setUp(self):
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

        self.obj = DummyModel(
            id=1,
            char_field="egg",
            text_field="ham",
            integer_field=10,
            datetime_field=datetime(2012, 4, 1, 10, 0, 0),
            date_field=date(2012, 4, 1),
            time_field=time(10, 0, 0),
            boolean_field=True)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'char_field': "egg",
            'text_field': "ham",
            'integer_field': 10,
            'datetime_field': datetime(2012, 4, 1, 10, 0, 0),
            'date_field': date(2012, 4, 1),
            'time_field': time(10, 0, 0),
            'boolean_field': True,
        })


class MetaFieldsTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        self.obj = DummyModel(id=1, spam="egg", bacon="ham")

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel
                fields = ['spam', 'bacon']

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'spam': "egg",
            'bacon': "ham",
        })


class MetaExcludeTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        self.obj = DummyModel(id=1, spam="egg", bacon="ham")

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel
                exclude = ['id', 'bacon']

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'spam': "egg",
        })


class AddFieldTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        self.obj = DummyModel(id=1, spam="egg", bacon="ham")

        class TestMapper(djangomodel.ModelMapper):
            knight = fields.StubField("ni")

            class Meta:
                model = DummyModel

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'spam': "egg",
            'bacon': "ham",
            'knight': "ni",
        })


class InheritedModelMapperOverrideFieldTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        self.obj = DummyModel(id=1, spam="egg", bacon="ham")

        class TestMapper(djangomodel.ModelMapper):
            spam = fields.StubField("knight")

            class Meta:
                model = DummyModel

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'spam': "knight",
            'bacon': "ham",
        })


class InheritedModelMapperTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        self.obj = DummyModel(id=1, spam="egg", bacon="ham")

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel

        class InheritedMapper(TestMapper):
            class Meta(TestMapper.Meta):
                pass

        self.mapper_class = InheritedMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'spam': "egg",
            'bacon': "ham",
        })


class CustomMapperFieldsTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        self.obj = DummyModel(id=1, spam="egg")

        class CustomMapperField(fields.RawField):
            def as_value(self, mapper, value):
                return "<%s>" % value

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel
                mapper_fields = {
                    models.CharField: CustomMapperField,
                }

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'spam': "<egg>",
        })


class CreateModelMapperTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        self.obj = DummyModel(id=1, spam="egg", bacon="ham")
        self.model_class = DummyModel

    def test_create_mapper(self):
        mapper_class = djangomodel.create_model_mapper(self.model_class)
        self.assertEqual(len(mapper_class._meta.fields), 3)
        self.assertTrue('id' in mapper_class._meta.fields)
        self.assertTrue('spam' in mapper_class._meta.fields)
        self.assertTrue('bacon' in mapper_class._meta.fields)
