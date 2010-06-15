# vim:fileencoding=utf-8
from copy import copy

from bpmappers.utils import MultiValueDict, SortedDict
from bpmappers.fields import Field, BaseField

class DataError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class Options(object):
    def __init__(self, *args, **kwargs):
        self.fields = MultiValueDict()
        # 重複チェック用のフィールド名リスト
        self.field_names = []

    def add_field(self, name, field):
        """
        フィールドを追加
        """
        if isinstance(field, Field) and field.key is None:
            field.key = name
        if name in self.field_names:
            # 既に登録されてる場合は削除する
            lst = self.fields.getlist(field.key)
            self.fields.setlist(field.key, [tp for tp in lst if tp[0] != name])
        else:
            self.field_names.append(name)
        self.fields.appendlist(field.key, (name, field))

    def copy(self):
        opt = Options()
        opt.fields = copy(self.fields)
        opt.field_names = copy(self.field_names)
        return opt

    def __repr__(self):
        return '<Options: %s>' % self.fields

class BaseMapper(type):
    def __new__(cls, name, bases, attrs):
        # copy bases
        opt = None
        for base_class in bases:
            if hasattr(base_class, '_meta'):
                base_meta = base_class._meta.copy()
                opt = base_meta
        if not '_meta' in attrs:
            if opt is None:
                opt = Options()
        else:
            opt = attrs['_meta'].copy()
        for k, v in attrs.iteritems():
            if isinstance(v, BaseField):
                # fieldsはMultiValueDict
                opt.add_field(k, v)
        attrs['_meta'] = opt
        return type.__new__(cls, name, bases, attrs)

class Mapper(object):
    __metaclass__ = BaseMapper
    default_options = {}

    def __init__(self, data=None, **options):
        self.data = data
        self.options = self.default_options
        self.options.update(options)

    def _getattr(self, obj, key):
        # attrを優先,なければスライスアクセス
        if not key:
            return
        if isinstance(obj, dict):
            return obj.get(key)
        else:
            try:
                return getattr(obj, key)
            except AttributeError:
                raise DataError('"%(obj)s" does not have this key "%(key)s in %(mapper)s"' % {'obj': obj, 'key': key, 'mapper': self})

    def as_dict(self):
        parsed = SortedDict()
        for k in self._meta.fields:
            # _meta.fieldsはMultiValue
            for name, field in self._meta.fields.getlist(k):
                if field.is_nonkey:
                    v = None
                elif isinstance(self.data, list):
                    # listだった場合は最初に取得できた要素を使う
                    data_check = False
                    error = None
                    for item in self.data:
                        try:
                            v = self._getattr(item, k)
                        except DataError, e:
                            error = e
                        else:
                            data_check = True
                            break
                    if not data_check:
                        raise DataError(error.message)
                else:
                    v = self._getattr(self.data, k)
                if callable(v):
                    v = v()
                filter_name = 'filter_%s' % name
                if hasattr(self, filter_name):
                    if field.is_nonkey:
                        v = getattr(self, filter_name)()
                    else:
                        v = getattr(self, filter_name)(v)
                parsed[name] = field.get_value(v)
                after_filter_name = 'after_filter_%s' % name
                if hasattr(self, after_filter_name):
                    parsed[name] = getattr(self, after_filter_name)(parsed[name])
        parsed.keyOrder = self._meta.field_names
        return parsed

    def __unicode__(self):
        return unicode(self.as_dict())
