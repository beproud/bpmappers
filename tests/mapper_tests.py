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
