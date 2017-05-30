from bpmappers.exceptions import InvalidDelegateException


class BaseField(object):
    def __init__(self, callback=None, after_callback=None, *args, **kwargs):
        self.key = None
        self._callback = callback
        self._after_callback = after_callback

    def callback_value(self, value):
        if self._callback is None:
            return value
        return self._callback(value)

    def after_callback_value(self, value):
        if self._after_callback is None:
            return value
        return self._after_callback(value)

    def get_value(self, mapper, value):
        return self.after_callback_value(
            self.as_value(mapper, self.callback_value(value)))

    def as_value(self, mapper, value):
        raise NotImplementedError

    @property
    def is_nonkey(self):
        raise NotImplementedError


class NonKeyField(BaseField):
    """Result values are generated manually.
    """
    def as_value(self, mapper, value=None):
        return value

    @property
    def is_nonkey(self):
        return True


class StubField(NonKeyField):
    """Result values are fixed value.
    """
    def __init__(self, stub={}, *args, **kwargs):
        self.stub = stub
        super(StubField, self).__init__(*args, **kwargs)

    def as_value(self, mapper, value=None):
        return self.stub


class Field(BaseField):
    """Basic class of Field.
    """
    def __init__(self, key=None, callback=None, skip_callable=False,
                 *args, **kwargs):
        super(Field, self).__init__(callback, *args, **kwargs)
        self.key = key
        self.skip_callable = skip_callable

    @property
    def is_nonkey(self):
        return False


class RawField(Field):
    """Result values are obtained from mapping source without conversion.
    """
    def as_value(self, mapper, value):
        return value


class ChoiceField(Field):
    def __init__(self, choices, key=None, callback=None, skip_callable=False,
                 *args, **kwargs):
        super(ChoiceField, self).__init__(
            key, callback, skip_callable, *args, **kwargs)
        self.choices = choices

    def as_value(self, mapper, value):
        # TODO: 2-value tuple iterator
        return self.choices[value]


class DelegateField(Field):
    """It is Field delegating mapping to the mapper_class.
    """
    def __init__(self, mapper_class, key=None, callback=None,
                 skip_callable=True, before_filter=None, required=True,
                 attach_parent=False, *args, **kwargs):
        super(DelegateField, self).__init__(
            key, callback, skip_callable, *args, **kwargs)
        self._before_filter = before_filter
        self.mapper_class = mapper_class
        self.required = required
        self.attach_parent = attach_parent

    def before_filter(self, value):
        if self._before_filter:
            return self._before_filter(value)
        return value

    def as_value(self, mapper, value):
        val = self.before_filter(value)
        if val is None:
            if not self.required:
                return
            raise InvalidDelegateException(
                'Invalid delegate "%(key)s" key in %(mapper)s.' % {
                    'key': self.key, 'mapper': mapper})
        return self.mapper_class(val, **mapper.options).as_dict()


class ListDelegateField(DelegateField):
    """Delegate mapping to mapper_class the value as list.
    """
    def __init__(self, mapper_class, key=None, callback=None, filter=None,
                 skip_callable=True, after_filter=None, *args, **kwargs):
        super(ListDelegateField, self).__init__(
            mapper_class, key, callback, skip_callable, *args, **kwargs)
        self._filter = filter
        self._after_filter = after_filter

    def filter(self, value):
        if self._filter:
            return self._filter(value)
        return value

    def after_filter(self, value):
        if self._after_filter:
            return self._after_filter(value)
        return value

    def as_value(self, mapper, value):
        parsed = []
        value = self.filter(value)
        if value is None:
            if not self.required:
                return
        # TODO: use iterator
        for v in value:
            parsed.append(self.after_filter(
                super(ListDelegateField, self).as_value(
                    mapper, self.callback_value(v))
            ))
        return parsed


class NonKeyDelegateField(NonKeyField):
    def __init__(self, mapper_class, callback=None, attach_parent=False,
                 *args, **kwargs):
        super(NonKeyDelegateField, self).__init__(callback, *args, **kwargs)
        self.mapper_class = mapper_class
        self.attach_parent = attach_parent

    def as_value(self, mapper, value=None):
        return self.mapper_class(value, **mapper.options).as_dict()


class NonKeyListDelegateField(NonKeyDelegateField):
    def __init__(self, mapper_class, callback=None, filter=None,
                 after_filter=None, *args, **kwargs):
        super(NonKeyListDelegateField, self).__init__(
            mapper_class, callback, *args, **kwargs)
        self._filter = filter
        self._after_filter = after_filter

    def filter(self, value=None):
        if self._filter:
            return self._filter(value)
        return value

    def after_filter(self, value):
        if self._after_filter:
            return self._after_filter(value)
        return value

    def as_value(self, mapper, value=[]):
        parsed = []
        value = self.filter(value)
        for v in value:
            parsed.append(self.after_filter(
                super(NonKeyListDelegateField, self).as_value(
                    mapper, self.callback_value(v))))
        return parsed
