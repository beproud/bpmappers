from .testing import TestCase, DummyObject, DummyCallback

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


class DelegateMappingAttachParentTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam=DummyObject(name="spam egg"))

        class TestMapper(mappers.Mapper):
            name = fields.RawField()

        class TestDelegate(mappers.Mapper):
            foo = fields.DelegateField(TestMapper, 'spam', attach_parent=True)

        self.mapper_class = TestDelegate

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'name': "spam egg",
        })


class NonKeyDelegateMappingTest(TestCase):
    def setUp(self):
        self.obj = {}

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')

        class TestDelegate(mappers.Mapper):
            bar = fields.NonKeyDelegateField(TestMapper)

            def filter_bar(self):
                return dict(spam="egg")

        self.mapper_class = TestDelegate

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'bar': {'foo': "egg"},
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


class DotAccessCallableTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(
            spam=DummyCallback(
                DummyObject(egg=DummyCallback('bacon'))
            )
        )

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam.egg')

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "bacon",
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


class MapperAttachMethodTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam="egg", bacon="ham")

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')

            def attach_foo(self, parsed, value):
                parsed["bar"] = value

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'bar': "egg",
        })


class MapperCallableValueTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam=DummyCallback("egg"))

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "egg",
        })


class MapperListValueTest(TestCase):
    def setUp(self):
        self.obj = [DummyObject(spam="egg")]

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'foo': "egg",
        })


class MapperOrderMethodTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam="egg", bacon="ham", knights="ni")

        class TestMapperBase(mappers.Mapper):
            spam = fields.RawField()
            bacon = fields.RawField()
            knights = fields.RawField()

        class TestOrderedA(TestMapperBase):
            def order(self, parsed):
                parsed.keyOrder = ['spam', 'bacon', 'knights']

        class TestOrderedB(TestMapperBase):
            def order(self, parsed):
                parsed.keyOrder = ['bacon', 'knights', 'spam']

        self.mapper_class_a = TestOrderedA
        self.mapper_class_b = TestOrderedB

    def test_mapping_a(self):
        mapper = self.mapper_class_a(self.obj)
        result = mapper.as_dict()
        self.assertEqual(list(result.keys()), ['spam', 'bacon', 'knights'])

    def test_mapping_b(self):
        mapper = self.mapper_class_b(self.obj)
        result = mapper.as_dict()
        self.assertEqual(list(result.keys()), ['bacon', 'knights', 'spam'])


class MapperKeyNameMethodTest(TestCase):
    def setUp(self):
        self.obj = DummyObject(spam="egg")

        class TestMapper(mappers.Mapper):
            foo = fields.RawField('spam')

            def key_name(self, name, value, field):
                return 'bar'

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'bar': "egg",
        })
