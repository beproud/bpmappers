import pytest

from .testing import DummyObject, DummyCallback

from bpmappers import fields
from bpmappers.utils import sort_dict_with_keys


class TestObjectToDictMapping:
    @pytest.fixture
    def data(self):
        return DummyObject(spam="egg", bacon="ham")

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')
            bar = fields.RawField('bacon')

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "egg",
            'bar': "ham",
        }
        assert result == expected


class TestDictToDictMapping:
    @pytest.fixture
    def data(self):
        return dict(spam="egg", bacon="ham")

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')
            bar = fields.RawField('bacon')

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "egg",
            'bar': "ham",
        }
        assert result == expected


class TestFieldFilterMethod:
    @pytest.fixture
    def data(self):
        return DummyObject(spam="egg", bacon="ham")

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')
            bar = fields.RawField('bacon')

            def filter_foo(self, value):
                return value.upper()

            def filter_bar(self, value):
                return "test"

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "EGG",
            'bar': "test",
        }
        assert result == expected


class TestFieldAfterFilterMethod:
    @pytest.fixture
    def data(self):
        return DummyObject(spam="egg", bacon="ham")

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')
            bar = fields.RawField('bacon')

            def after_filter_foo(self, value):
                return value.upper()

            def after_filter_bar(self, value):
                return "test"

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "EGG",
            'bar': "test",
        }
        assert result == expected


class TestDelegateMapping:
    @pytest.fixture
    def data(self):
        return DummyObject(
            spam=DummyObject(name="spam egg"),
            bacon=DummyObject(name="bacon egg"))

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            "name --> egg_name"
            egg_name = fields.RawField('name')

        class TestDelegate(Mapper):
            "spam -(TestMapper)-> spam_egg"
            spam_egg = fields.DelegateField(TestMapper, 'spam')
            bacon_egg = fields.DelegateField(TestMapper, 'bacon')

        return TestDelegate

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'spam_egg': {'egg_name': "spam egg"},
            'bacon_egg': {'egg_name': "bacon egg"},
        }
        assert result == expected


class TestDelegateMappingAttachParent:
    @pytest.fixture
    def data(self):
        return DummyObject(spam=DummyObject(name="spam egg"))

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            name = fields.RawField()

        class TestDelegate(Mapper):
            foo = fields.DelegateField(TestMapper, 'spam', attach_parent=True)

        return TestDelegate

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'name': "spam egg",
        }
        assert result == expected


class TestNonKeyDelegateMapping:
    @pytest.fixture
    def data(self):
        return {}

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')

        class TestDelegate(Mapper):
            bar = fields.NonKeyDelegateField(TestMapper)

            def filter_bar(self):
                return dict(spam="egg")

        return TestDelegate

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'bar': {'foo': "egg"},
        }
        assert result == expected


class TestInheritedMapperAddField:
    @pytest.fixture
    def data(self):
        return DummyObject(spam="egg", bacon="ham")

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')

        class InheritedMapper(TestMapper):
            bar = fields.RawField('bacon')

        return InheritedMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "egg",
            'bar': "ham",
        }
        assert result == expected


class TestInheritedMapperOverrideField:
    @pytest.fixture
    def data(self):
        return DummyObject(spam="egg", bacon="ham")

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')

        class InheritedMapper(TestMapper):
            foo = fields.RawField('bacon')

        return InheritedMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "ham",
        }
        assert result == expected


class TestDotAccessValue:
    @pytest.fixture
    def data(self):
        return {"spam": {"egg": {"bacon": "ham"}}}

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam.egg.bacon')

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "ham",
        }
        assert result == expected


class TestDotAccessCallable:
    @pytest.fixture
    def data(self):
        return DummyObject(
            spam=DummyCallback(
                DummyObject(egg=DummyCallback('bacon'))
            )
        )

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam.egg')

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "bacon",
        }
        assert result == expected


class TestOptionsParameter:
    @pytest.fixture
    def data(self):
        return DummyObject()

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            spam = fields.NonKeyField()

            def filter_spam(self):
                return self.options.get('bacon')

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data, bacon="egg")
        result = mapper.as_dict()
        expected = {
            'spam': "egg",
        }
        assert result == expected


class TestMapperAttachMethod:
    @pytest.fixture
    def data(self):
        return DummyObject(spam="egg", bacon="ham")

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')

            def attach_foo(self, parsed, value):
                parsed["bar"] = value

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'bar': "egg",
        }
        assert result == expected


class TestMapperCallableValue:
    @pytest.fixture
    def data(self):
        return DummyObject(spam=DummyCallback("egg"))

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "egg",
        }
        assert result == expected


class TestMapperListValue:
    @pytest.fixture
    def data(self):
        return [DummyObject(spam="egg")]

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'foo': "egg",
        }
        assert result == expected


class TestMapperOrderMethod:
    @pytest.fixture
    def data(self):
        return DummyObject(spam="egg", bacon="ham", knights="ni")

    @pytest.fixture
    def base(self):
        from bpmappers.mappers import Mapper

        class TestMapperBase(Mapper):
            spam = fields.RawField()
            bacon = fields.RawField()
            knights = fields.RawField()

        return TestMapperBase

    @pytest.fixture
    def target_a(self, base):

        class TestOrderedA(base):
            def order(self, parsed):
                return sort_dict_with_keys(
                    parsed, ['spam', 'bacon', 'knights'])

        return TestOrderedA

    @pytest.fixture
    def target_b(self, base):

        class TestOrderedB(base):
            def order(self, parsed):
                return sort_dict_with_keys(
                    parsed, ['bacon', 'knights', 'spam'])

        return TestOrderedB

    def test_mapping_a(self, target_a, data):
        mapper = target_a(data)
        result = mapper.as_dict()
        expected = ['spam', 'bacon', 'knights']
        assert list(result.keys()) == expected

    def test_mapping_b(self, target_b, data):
        mapper = target_b(data)
        result = mapper.as_dict()
        expected = ['bacon', 'knights', 'spam']
        assert list(result.keys()) == expected


class TestMapperKeyNameMethod:
    @pytest.fixture
    def data(self):
        return DummyObject(spam="egg")

    @pytest.fixture
    def target(self):
        from bpmappers.mappers import Mapper

        class TestMapper(Mapper):
            foo = fields.RawField('spam')

            def key_name(self, name, value, field):
                return 'bar'

        return TestMapper

    def test_mapping(self, target, data):
        mapper = target(data)
        result = mapper.as_dict()
        expected = {
            'bar': "egg",
        }
        assert result == expected
