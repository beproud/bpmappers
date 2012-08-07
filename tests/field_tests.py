from testing import TestCase, DummyCallback

from bpmappers import fields
from bpmappers.exceptions import InvalidDelegateException


class NonKeyFieldTest(TestCase):
    "Tests for NonKeyField class."
    def setUp(self):
        self.callback = DummyCallback(returns="Spam")
        self.field = fields.NonKeyField(self.callback)

    def test_get_value(self):
        value = self.field.get_value(None, None)
        self.assertEqual(value, self.callback.returns)

    def test_as_value(self):
        value = self.field.as_value(None, "Egg")
        self.assertEqual(value, "Egg")

    def test_is_nonkey(self):
        self.assertEqual(self.field.is_nonkey, True)


class StubFieldTest(TestCase):
    "Tests for StubField class."
    def setUp(self):
        self.field = fields.StubField("Spam")

    def test_as_value(self):
        value = self.field.as_value(None)
        self.assertEqual(value, "Spam")

    def test_is_nonkey(self):
        self.assertEqual(self.field.is_nonkey, True)


class RawFieldTest(TestCase):
    "Tests for RawField class."
    def setUp(self):
        self.field = fields.RawField(key="SpamKey")

    def test_get_value(self):
        value = self.field.get_value(None, "Egg")
        self.assertEqual(value, "Egg")

    def test_is_nonkey(self):
        self.assertEqual(self.field.is_nonkey, False)


class ChoiceFieldTest(TestCase):
    "Tests for ChoiceField class."
    def setUp(self):
        self.field = fields.ChoiceField(
            choices={1: "Spam", 2: "Egg", 3: "Bacon"})

    def test_get_value(self):
        value1 = self.field.get_value(None, 1)
        self.assertEqual(value1, "Spam")
        value2 = self.field.get_value(None, 2)
        self.assertEqual(value2, "Egg")
        value3 = self.field.get_value(None, 3)
        self.assertEqual(value3, "Bacon")

    def test_is_nonkey(self):
        self.assertEqual(self.field.is_nonkey, False)


class DummyMapper(object):
    def __init__(self, value, **options):
        self.value = value
        self.options = options

    def as_dict(self):
        return self.value


class DelegateFieldTest(TestCase):
    "Tests for DelegateField class."
    def setUp(self):
        self.field = fields.DelegateField(DummyMapper)

    def test_get_value(self):
        value = self.field.get_value(
            DummyMapper(None), {"Spam": "Egg"})
        self.assertEqual(value, {"Spam": "Egg"})

    def test_invalid(self):
        self.assertRaises(
            InvalidDelegateException,
            self.field.get_value,
            DummyMapper(None),
            None)

    def test_is_nonkey(self):
        self.assertEqual(self.field.is_nonkey, False)


class DelegateFieldBeforeFilterTest(TestCase):
    "DelegateField._before_filter"
    def setUp(self):
        self.field = fields.DelegateField(
            DummyMapper, before_filter=lambda v: {1: "Spam"})

    def test_get_value(self):
        value = self.field.get_value(
            DummyMapper(None), None)
        self.assertEqual(value, {1: "Spam"})


class DelegateFieldRequiredTest(TestCase):
    "DelegateField.required=False"
    def setUp(self):
        self.field = fields.DelegateField(
            DummyMapper, required=False)

    def test_none_value(self):
        value = self.field.get_value(DummyMapper(None), None)
        self.assertEqual(value, None)
