# -*- coding: utf-8 -*-
from copy import copy

from bpmappers.utils import MultiValueDict, SortedDict
from bpmappers.fields import Field, BaseField
from bpmappers.exceptions import DataError

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
        self.options = self.default_options.copy()
        self.options.update(options)

    def _getattr_inner(self, obj, key):
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

    def _getattr(self, obj, key):
        # ドットアクセスの場合は再帰
        if '.' in key:
            keys = key.split('.')
            obj_child = self._getattr(obj, keys[0])
            value = self._getattr(obj_child, '.'.join(keys[1:]))
        else:
            value = self._getattr_inner(obj, key)
        return value

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
                value = field.get_value(self, v)
                # after filter hook
                after_filter_name = 'after_filter_%s' % name
                if hasattr(self, after_filter_name):
                    value = getattr(self, after_filter_name)(value)
                # attach hook
                attach_name = 'attach_%s' % name
                if hasattr(self, attach_name):
                    getattr(self, attach_name)(parsed, value)
                else:
                    attach_parent = getattr(field, 'attach_parent', False)
                    if attach_parent:
                        parsed.update(value)
                    else:
                        parsed[self.key_name(name, value, field)] = value
        self.order(parsed)
        return parsed

    def order(self, parsed):
        def _cmp(x, y):
            if x in self._meta.field_names:
                x_pos = self._meta.field_names.index(x)
            else:
                x_pos = -1
            if y in self._meta.field_names:
                y_pos = self._meta.field_names.index(y)
            else:
                y_pos = -1
            return cmp(x_pos, y_pos)
        parsed.keyOrder = sorted(parsed.keyOrder, cmp=_cmp)

    def key_name(self, name, value, field):
        """
        hook point for key name convert.
        """
        return name

    def __unicode__(self):
        return unicode(self.as_dict())
