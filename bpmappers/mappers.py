from copy import copy
from collections import OrderedDict, defaultdict

import six

from bpmappers.utils import sort_dict_with_keys
from bpmappers.fields import Field, BaseField
from bpmappers.exceptions import DataError


class Options(object):
    """Meta data of Mapper.
    """
    def __init__(self, *args, **kwargs):
        self.fields = defaultdict(list)
        # Use this list to checking for existing name.
        self.field_names = []

    def add_field(self, name, field):
        """Add field"""
        if isinstance(field, Field) and field.key is None:
            field.key = name
        if name in self.field_names:
            # if the field is already registered, remove it.
            lst = self.fields[field.key]
            self.fields[field.key] = [tp for tp in lst if tp[0] != name]
            for key in list(self.fields.keys()):
                lst = self.fields[key]
                updated_lst = [tp for tp in lst if tp[0] != name]
                if updated_lst:
                    self.fields[key] = [tp for tp in lst if tp[0] != name]
                else:
                    del self.fields[key]
        else:
            self.field_names.append(name)
        self.fields[field.key].append((name, field))

    def copy(self):
        opt = Options()
        opt.fields = copy(self.fields)
        opt.field_names = copy(self.field_names)
        return opt

    def __repr__(self):
        return '<Options: %s>' % self.fields


class BaseMapper(type):
    """Metaclass of Mapper.
    """
    def __new__(cls, name, bases, attrs):
        # copy bases
        opt = None
        base_opts = []
        for base_class in bases:
            if hasattr(base_class, '_meta'):
                base_opt = base_class._meta.copy()
                base_opts.append(base_opt)
        if '_meta' not in attrs:
            if opt is None:
                opt = Options()
        else:
            opt = attrs['_meta'].copy()
        # Merge bases
        for base_opt in base_opts:
            for key in base_opt.fields.keys():
                lst = base_opt.fields[key]
                for _name, field in lst:
                    opt.add_field(_name, field)
        for k, v in attrs.items():
            if isinstance(v, BaseField):
                opt.add_field(k, v)
        attrs['_meta'] = opt
        return type.__new__(cls, name, bases, attrs)


class Mapper(six.with_metaclass(BaseMapper)):
    """Basic Mapper class.
    """
    default_options = {}

    def __init__(self, data=None, **options):
        """
        :data: Mapping source object.
        :\*\*options: Optional values.
        """
        self.data = data
        self.options = self.default_options.copy()
        self.options.update(options)

    def _getattr_inner(self, obj, key):
        # Priority "attr", "dict", "getattr".
        if not key:
            return
        if isinstance(obj, dict):
            return obj.get(key)
        else:
            try:
                return getattr(obj, key)
            except AttributeError:
                raise DataError(
                    '"%(obj)s" does not have this key'
                    ' "%(key)s in %(mapper)s"' % {
                        'obj': obj, 'key': key, 'mapper': repr(self)})

    def _getattr(self, obj, key):
        # Recursive call if it is dot splited accessor.
        if '.' in key:
            keys = key.split('.')
            obj_child = self._getattr(obj, keys[0])
            # If child object is callable, call that object.
            if hasattr(obj_child, '__call__'):
                obj_child = obj_child()
            value = self._getattr(obj_child, '.'.join(keys[1:]))
        else:
            value = self._getattr_inner(obj, key)
        return value

    def as_dict(self):
        """
        Return the OrderedDict it is mapping result.
        """
        parsed = OrderedDict()
        for k in self._meta.fields:
            # _meta.fields is MultiValueDict
            for name, field in self._meta.fields[k]:
                if field.is_nonkey:
                    v = None
                elif isinstance(self.data, list):
                    # if data is list, use first.
                    data_check = False
                    error = None
                    for item in self.data:
                        try:
                            v = self._getattr(item, k)
                        except DataError:
                            import sys
                            error = sys.exc_info()[1]
                        else:
                            data_check = True
                            break
                    if not data_check:
                        raise DataError(error.message)
                else:
                    v = self._getattr(self.data, k)
                if hasattr(v, '__call__') and not field.skip_callable:
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
        ordered = self.order(parsed)
        return ordered

    def order(self, parsed):
        """
        This method **must** return the OrderedDict.
        """
        return sort_dict_with_keys(parsed, self._meta.field_names)

    def key_name(self, name, value, field):
        """
        Hook point for key name converting.
        """
        return name

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self)

    def __str__(self):
        return str(', '.join(self._meta.field_names))
