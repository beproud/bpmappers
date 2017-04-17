import pytest

from .testing import DummyCallback


class TestBaseField:
    "Tests for BaseField class."
    @pytest.fixture
    def target(self):
        from bpmappers.fields import BaseField
        return BaseField()

    def test_implementation_required(self, target):
        with pytest.raises(NotImplementedError):
            target.is_nonkey()
        with pytest.raises(NotImplementedError):
            target.as_value(None, None)


class TestNonKeyField:
    "Tests for NonKeyField class."
    @pytest.fixture
    def callback(self):
        return DummyCallback("Spam")

    def target(self, callback):
        from bpmappers.fields import NonKeyField
        return NonKeyField(callback)

    def test_get_value(self, callback):
        target = self.target(callback)
        value = target.get_value(None, None)
        assert callback.called
        assert value == callback.returns

    def test_is_nonkey(self, callback):
        target = self.target(callback)
        assert target.is_nonkey


class TestStubField:
    "Tests for StubField class."
    @pytest.fixture
    def target(self):
        from bpmappers.fields import StubField
        return StubField("Spam")

    def test_as_value(self, target):
        value = target.as_value(None)
        assert value == "Spam"

    def test_is_nonkey(self, target):
        assert target.is_nonkey


class TestRawField:
    "Tests for RawField class."
    @pytest.fixture
    def target(self):
        from bpmappers.fields import RawField
        return RawField(key="SpamKey")

    def test_get_value(self, target):
        value = target.get_value(None, "Egg")
        assert value == "Egg"

    def test_is_nonkey(self, target):
        assert not target.is_nonkey


class TestAfterCallback:
    "Tests for after_callback"
    @pytest.fixture
    def callback(self):
        return DummyCallback("Spam")

    def target(self, callback):
        from bpmappers.fields import NonKeyField
        return NonKeyField(after_callback=callback)

    def test_get_value(self, callback):
        target = self.target(callback)
        value = target.get_value(None, None)
        assert value == "Spam"


class TestChoiceField:
    "Tests for ChoiceField class."
    @pytest.fixture
    def target(self):
        from bpmappers.fields import ChoiceField
        return ChoiceField(choices={1: "Spam", 2: "Egg", 3: "Bacon"})

    def test_get_value(self, target):
        value1 = target.get_value(None, 1)
        assert value1 == "Spam"
        value2 = target.get_value(None, 2)
        assert value2 == "Egg"
        value3 = target.get_value(None, 3)
        assert value3 == "Bacon"

    def test_is_nonkey(self, target):
        assert not target.is_nonkey


class DummyMapper:
    def __init__(self, value, **options):
        self.value = value
        self.options = options

    def as_dict(self):
        return self.value


class TestDelegateField:
    "Tests for DelegateField class."
    @pytest.fixture
    def target(self):
        from bpmappers.fields import DelegateField
        return DelegateField(DummyMapper)

    def test_get_value(self, target):
        value = target.get_value(
            DummyMapper(None), {"Spam": "Egg"})
        assert value == {"Spam": "Egg"}

    def test_invalid(self, target):
        from bpmappers.exceptions import InvalidDelegateException
        with pytest.raises(InvalidDelegateException):
            target.get_value(DummyMapper(None), None)

    def test_is_nonkey(self, target):
        assert not target.is_nonkey


class TestDelegateFieldBeforeFilter:
    "DelegateField._before_filter"
    @pytest.fixture
    def before_filter(self):
        return DummyCallback({1: "Spam"})

    def target(self, before_filter):
        from bpmappers.fields import DelegateField
        return DelegateField(
            DummyMapper, before_filter=before_filter)

    def test_get_value(self, before_filter):
        target = self.target(before_filter)
        value = target.get_value(DummyMapper(None), None)
        assert value == before_filter.returns
        assert before_filter.called


class TestDelegateFieldRequired:
    "DelegateField.required=False"
    @pytest.fixture
    def target(self):
        from bpmappers.fields import DelegateField
        return DelegateField(
            DummyMapper, required=False)

    def test_none_value(self, target):
        value = target.get_value(DummyMapper(None), None)
        assert value is None


class TestListDelegateField:
    "Test for ListDelegateField class."
    @pytest.fixture
    def target(self):
        from bpmappers.fields import ListDelegateField
        return ListDelegateField(DummyMapper)

    def test_get_value(self, target):
        # TODO: need more
        value = target.get_value(
            DummyMapper(None), [{"Spam": "Egg"}, {"Bacon": "Egg"}])
        assert value == [{"Spam": "Egg"}, {"Bacon": "Egg"}]

    def test_is_nonkey(self, target):
        assert not target.is_nonkey


class TestListDelegateFieldFilter:
    "ListDelegateField.filter"
    @pytest.fixture
    def filter(self):
        return DummyCallback([1, 2, 3])

    def target(self, filter):
        from bpmappers.fields import ListDelegateField
        return ListDelegateField(DummyMapper, filter=filter)

    def test_get_value(self, filter):
        target = self.target(filter)
        value = target.get_value(DummyMapper(None), [])
        assert value == [1, 2, 3]
        assert filter.called


class TestListDelegateFieldAfterFilter:
    "ListDelegateField.after_filter"
    @pytest.fixture
    def after_filter(self):
        return DummyCallback("Spam")

    def target(self, after_filter):
        from bpmappers.fields import ListDelegateField
        return ListDelegateField(DummyMapper, after_filter=after_filter)

    def test_get_value(self, after_filter):
        target = self.target(after_filter)
        value = target.get_value(
            DummyMapper(None), [1, 2, 3])
        assert value == ["Spam", "Spam", "Spam"]
        assert after_filter.called


class TestNonKeyDelegateField:
    "Test for NonKeyDelegateField class."
    @pytest.fixture
    def callback(self):
        return DummyCallback({"Spam": "Egg"})

    @pytest.fixture
    def target(self, callback):
        from bpmappers.fields import NonKeyDelegateField
        return NonKeyDelegateField(DummyMapper, callback=callback)

    def test_get_value(self, callback):
        target = self.target(callback)
        value = target.get_value(DummyMapper(None), None)
        assert value == callback.returns
        assert callback.called

    def test_is_nonkey(self, target):
        assert target.is_nonkey


class TestNonKeyListDelegateField:
    "Test for NonKeyListDelegateField class."
    @pytest.fixture
    def callback(self):
        return DummyCallback({"Spam": "Egg"})

    @pytest.fixture
    def target(self, callback):
        from bpmappers.fields import NonKeyListDelegateField
        return NonKeyListDelegateField(DummyMapper, callback=callback)

    def test_get_value(self, callback):
        target = self.target(callback)
        value = target.get_value(DummyMapper(None), None)
        assert value == [callback.returns]
        assert callback.called

    def test_is_nonkey(self, target):
        assert target.is_nonkey


class TestNonKeyListDelegateFieldFilter:
    "NonKeyListDelegateField.filter"
    @pytest.fixture
    def filter(self):
        return DummyCallback([1, 2, 3])

    def target(self, filter):
        from bpmappers.fields import NonKeyListDelegateField
        return NonKeyListDelegateField(DummyMapper, filter=filter)

    def test_get_value(self, filter):
        target = self.target(filter)
        value = target.get_value(DummyMapper(None), [{"Spam": "Egg"}])
        assert value == filter.returns
        assert filter.called


class TestNonKeyListDelegateFieldAfterFilter:
    "NonKeyListDelegateField.after_filter"
    @pytest.fixture
    def after_filter(self):
        return DummyCallback("Spam")

    def target(self, after_filter):
        from bpmappers.fields import NonKeyListDelegateField
        return NonKeyListDelegateField(DummyMapper, after_filter=after_filter)

    def test_get_value(self, after_filter):
        target = self.target(after_filter)
        value = target.get_value(
            DummyMapper(None), [1, 2, 3])
        assert value == ["Spam", "Spam", "Spam"]
        assert after_filter.called
