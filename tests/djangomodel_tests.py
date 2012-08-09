from datetime import datetime, date, time

from . import testing_django

from .testing import TestCase, DummyObject, SkipTest

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


class DjangoFileFieldTest(TestCase):
    def setUp(self):
        self.field = djangomodel.DjangoFileField()
        self.obj = DummyObject(url="egg")

    def test_url(self):
        value = self.field.get_value(None, self.obj)
        self.assertEqual(value, "egg")

    def test_none(self):
        value = self.field.get_value(None, None)
        self.assertIsNone(value)


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


class ForeignKeyFieldModelMapperTest(TestCase):
    def setUp(self):
        class ChildModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class ParentModel(models.Model):
            bacon = models.ForeignKey(ChildModel)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = ParentModel

        self.child = ChildModel(id=1, spam="egg")
        self.parent = ParentModel(id=1, bacon=self.child)
        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.parent)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'bacon': {
                'id': 1,
                'spam': "egg",
            },
        })


class ForeignKeyFieldNullValueTest(TestCase):
    def setUp(self):
        class ChildModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class ParentModel(models.Model):
            bacon = models.ForeignKey(ChildModel, null=True, blank=True)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = ParentModel

        self.parent = ParentModel(id=1, bacon=None)
        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.parent)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'bacon': None,
        })


class ForeignKeySelfReferenceTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.ForeignKey("DummyModel", null=True, blank=True)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel

        self.obj = DummyModel(id=1)
        self.obj.spam = DummyModel(id=2)
        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
        })


class OneToOneFieldModelMappingTest(TestCase):
    def setUp(self):
        class ChildModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class ParentModel(models.Model):
            bacon = models.OneToOneField(ChildModel)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = ParentModel

        child = ChildModel(id=1, spam="egg")
        self.parent = ParentModel(id=1, bacon=child)
        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.parent)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'bacon': {
                'id': 1,
                'spam': "egg",
            },
        })


class ManyToManyFieldModelMapperTest(TestCase):
    def setUp(self):
        class ChildModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class ParentModel(models.Model):
            bacon = models.ManyToManyField(ChildModel)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        testing_django._setup_db()
        testing_django.create_table(ChildModel)
        testing_django.create_table(ParentModel)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = ParentModel

        child = ChildModel(id=1, spam="egg")
        child.save()
        self.parent = ParentModel(id=1)
        self.parent.save()
        self.parent.bacon.add(child)
        self.mapper_class = TestMapper

    def tearDown(self):
        testing_django._teardown_db()

    def test_mapping(self):
        mapper = self.mapper_class(self.parent)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'bacon': [
                {
                    'id': 1,
                    'spam': "egg",
                }
            ],
        })


class ManyToManyFieldThroughModelTest(TestCase):
    def setUp(self):
        class ChildModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class ParentModel(models.Model):
            bacon = models.ManyToManyField(ChildModel, through="ThroughModel")

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class ThroughModel(models.Model):
            child = models.ForeignKey(ChildModel)
            parent = models.ForeignKey(ParentModel)
            knight = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        testing_django._setup_db()
        testing_django.create_table(ChildModel)
        testing_django.create_table(ParentModel)
        if testing_django.get_django_version() < (1, 2):
            testing_django.create_table(ThroughModel)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = ThroughModel

        child = ChildModel(id=1, spam="egg")
        child.save()
        parent = ParentModel(id=1)
        parent.save()
        self.through = ThroughModel(
            id=1, child=child, parent=parent, knight="ni")
        self.through.save()
        self.mapper_class = TestMapper

    def tearDown(self):
        testing_django._teardown_db()

    def test_mapping(self):
        mapper = self.mapper_class(self.through)
        result = mapper.as_dict()
        self.assertEqual(result, {
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
        })


class CustomFieldTest(TestCase):
    def setUp(self):
        class CustomField(models.Field):
            pass

        class DummyModel(models.Model):
            spam = CustomField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel

        self.obj = DummyModel(id=1, spam="egg")
        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'spam': "egg",
        })


class FileFieldModelMapperTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.FileField(upload_to='./')

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel

        self.obj = DummyModel(id=1)
        # django 1.0.x is not able to set name attribute.
        if testing_django.get_django_version() < (1, 1):
            self.obj.spam._name = 'egg.txt'
        else:
            self.obj.spam.name = 'egg.txt'
        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'spam': "egg.txt",
        })


class ImageFieldModelMapperTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.ImageField(upload_to='./')

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel

        self.obj = DummyModel(id=1)
        # django 1.0.x is not able to set name attribute.
        if testing_django.get_django_version() < (1, 1):
            self.obj.spam._name = 'egg.jpg'
        else:
            self.obj.spam.name = 'egg.jpg'
        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'spam': "egg.jpg",
        })


class MixinModelMapperTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)

            class Meta:
                app_label = testing_django.lower_class_name(self)

        class TestMapper(mappers.Mapper):
            knight = fields.StubField("ni")

        class MixinMapper(TestMapper, djangomodel.ModelMapper):

            class Meta:
                model = DummyModel

        self.obj = DummyModel(id=1, spam="egg")
        self.mapper_class = MixinMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'spam': "egg",
            'knight': "ni",
        })
