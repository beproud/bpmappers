from .testing import TestCase, DummyCallback

from bpmappers import fields
from bpmappers.exceptions import InvalidDelegateException


class BaseFieldTest(TestCase):
    "Tests for BaseField class."
    def setUp(self):
        self.field = fields.BaseField()

    def test_implementation_required(self):
        self.assertRaises(NotImplementedError, lambda :self.field.is_nonkey)
        self.assertRaises(NotImplementedError, self.field.as_value, None, None)


class NonKeyFieldTest(TestCase):
    "Tests for NonKeyField class."
    def setUp(self):
        self.callback = DummyCallback("Spam")
        self.field = fields.NonKeyField(self.callback)

    def test_get_value(self):
        value = self.field.get_value(None, None)
        self.assertTrue(self.callback.called)
        self.assertEqual(value, self.callback.returns)

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


class AfterCallbackTest(TestCase):
    "Tests for after_callback"
    def setUp(self):
        self.callback = DummyCallback("Spam")
        self.field = fields.NonKeyField(after_callback=self.callback)

    def test_get_value(self):
        value = self.field.get_value(None, None)
        self.assertEqual(value, "Spam")


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
        self.before_filter = DummyCallback({1: "Spam"})
        self.field = fields.DelegateField(
            DummyMapper, before_filter=self.before_filter)

    def test_get_value(self):
        value = self.field.get_value(
            DummyMapper(None), None)
        self.assertEqual(value, self.before_filter.returns)
        self.assertTrue(self.before_filter.called)


class DelegateFieldRequiredTest(TestCase):
    "DelegateField.required=False"
    def setUp(self):
        self.field = fields.DelegateField(
            DummyMapper, required=False)

    def test_none_value(self):
        value = self.field.get_value(DummyMapper(None), None)
        self.assertEqual(value, None)


class ListDelegateFieldTest(TestCase):
    "Test for ListDelegateField class."
    def setUp(self):
        self.field = fields.ListDelegateField(DummyMapper)

    def test_get_value(self):
        # TODO: need more
        value = self.field.get_value(
            DummyMapper(None), [{"Spam": "Egg"}, {"Bacon": "Egg"}])
        self.assertEqual(value, [{"Spam": "Egg"}, {"Bacon": "Egg"}])

    def test_is_nonkey(self):
        self.assertEqual(self.field.is_nonkey, False)


class ListDelegateFieldFilterTest(TestCase):
    "ListDelegateField.filter"
    def setUp(self):
        self.filter = DummyCallback([1, 2, 3])
        self.field = fields.ListDelegateField(DummyMapper, filter=self.filter)

    def test_get_value(self):
        value = self.field.get_value(
            DummyMapper(None), [])
        self.assertEqual(value, [1, 2, 3])
        self.assertTrue(self.filter.called)


class ListDelegateFieldAfterFilterTest(TestCase):
    "ListDelegateField.after_filter"
    def setUp(self):
        self.after_filter = DummyCallback("Spam")
        self.field = fields.ListDelegateField(
            DummyMapper,
            after_filter=self.after_filter)

    def test_get_value(self):
        value = self.field.get_value(
            DummyMapper(None), [1, 2, 3])
        self.assertEqual(value, ["Spam", "Spam", "Spam"])
        self.assertTrue(self.after_filter.called)


class NonKeyDelegateFieldTest(TestCase):
    "Test for NonKeyDelegateField class."
    def setUp(self):
        self.callback = DummyCallback({"Spam": "Egg"})
        self.field = fields.NonKeyDelegateField(
            DummyMapper, callback=self.callback)

    def test_get_value(self):
        value = self.field.get_value(DummyMapper(None), None)
        self.assertEqual(value, self.callback.returns)
        self.assertTrue(self.callback.called)

    def test_is_nonkey(self):
        self.assertEqual(self.field.is_nonkey, True)


class NonKeyListDelegateFieldTest(TestCase):
    "Test for NonKeyListDelegateField class."
    def setUp(self):
        self.callback = DummyCallback({"Spam": "Egg"})
        self.field = fields.NonKeyListDelegateField(
            DummyMapper, callback=self.callback)

    def test_get_value(self):
        value = self.field.get_value(DummyMapper(None), None)
        self.assertEqual(value, [self.callback.returns])
        self.assertTrue(self.callback.called)

    def test_is_nonkey(self):
        self.assertEqual(self.field.is_nonkey, True)


class NonKeyListDelegateFieldFilterTest(TestCase):
    "NonKeyListDelegateField.filter"
    def setUp(self):
        self.filter = DummyCallback([1, 2, 3])
        self.field = fields.NonKeyListDelegateField(
            DummyMapper, filter=self.filter)

    def test_get_value(self):
        value = self.field.get_value(DummyMapper(None), [{"Spam": "Egg"}])
        self.assertEqual(value, self.filter.returns)
        self.assertTrue(self.filter.called)


class NonKeyListDelegateFieldAfterFilterTest(TestCase):
    "NonKeyListDelegateField.after_filter"
    def setUp(self):
        self.after_filter = DummyCallback("Spam")
        self.field = fields.NonKeyListDelegateField(
            DummyMapper,
            after_filter=self.after_filter)

    def test_get_value(self):
        value = self.field.get_value(
            DummyMapper(None), [1, 2, 3])
        self.assertEqual(value, ["Spam", "Spam", "Spam"])
        self.assertTrue(self.after_filter.called)
