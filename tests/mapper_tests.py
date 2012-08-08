from testing import TestCase, DummyObject

from bpmappers import fields
from bpmappers import mappers


class ObjectToDictMappingTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam="egg", bacon="ham")

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')
            bar = fields.RawField('bacon')

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "egg",
            'bar': "ham",
        })


class DictToDictMappingTest(TestCase):
    def setUp(self):
        self.obj = dict(spam="egg", bacon="ham")

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')
            bar = fields.RawField('bacon')

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "egg",
            'bar': "ham",
        })


class FieldFilterMethodTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam="egg", bacon="ham")

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')
            bar = fields.RawField('bacon')

            def filter_foo(self, value):
                return value.upper()

            def filter_bar(self, value):
                return "test"

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "EGG",
            'bar': "test",
        })


class FieldAfterFilterMethodTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam="egg", bacon="ham")

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')
            bar = fields.RawField('bacon')

            def after_filter_foo(self, value):
                return value.upper()

            def after_filter_bar(self, value):
                return "test"

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "EGG",
            'bar': "test",
        })


class DelegateMappingTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(
            spam=DummyObject(name="spam egg"),
            bacon=DummyObject(name="bacon egg"))

        class TestMapper(mappers.Mapper):
            "name --> egg_name"
            egg_name = fields.RawField('name')

        class TestDelegate(mappers.Mapper):
            "spam -(TestMapper)-> spam_egg"
            spam_egg = fields.DelegateField(TestMapper, 'spam')
            bacon_egg = fields.DelegateField(TestMapper, 'bacon')

        self.mapper_class = TestDelegate

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'spam_egg': {'egg_name': "spam egg"},
            'bacon_egg': {'egg_name': "bacon egg"},
        })


class InheritedMapperAddFieldTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam="egg", bacon="ham")

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')

        class InheritedMapper(TestMapper):
            bar = fields.RawField('bacon')

        self.mapper_class = InheritedMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "egg",
            'bar': "ham",
        })


class InheritedMapperOverrideFieldTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam="egg", bacon="ham")

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')

        class InheritedMapper(TestMapper):
            foo = fields.RawField('bacon')

        self.mapper_class = InheritedMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "ham",
        })


class DotAccessValueTest(TestCase):
    def setUp(self):
        self.obj = {"spam": {"egg": {"bacon": "ham"}}}

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam.egg.bacon')

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "ham",
        })


class OptionsParameterTest(TestCase):
    def setUp(self):
        self.obj = DummyObject()

        class TestMapper(mappers.Mapper):
            spam = fields.NonKeyField()

            def filter_spam(self):
                return self.options.get('bacon')

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj, bacon="egg")
        result = mapper.as_dict()
        self.assertEqual(result, {
            'spam': "egg",
        })
