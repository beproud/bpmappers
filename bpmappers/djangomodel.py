# -*- coding: utf-8 -*-
import six

from bpmappers.fields import Field, RawField, DelegateField, ListDelegateField
from bpmappers.mappers import Options, BaseMapper, Mapper

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class MetaModelError(Exception):
    "Invalid mapper Meta"


class DjangoFileField(Field):
    def as_value(self, mapper, value):
        return value and value.url or None


DEFAULT_MAPPER_FIELD = RawField

# Mapping Django model field to MaperField.
DEFINED_MODEL_MAPPER_FIELDS = {
    models.AutoField: DEFAULT_MAPPER_FIELD,
    models.CharField: DEFAULT_MAPPER_FIELD,
    models.TextField: DEFAULT_MAPPER_FIELD,
    models.IntegerField: DEFAULT_MAPPER_FIELD,
    models.DateTimeField: DEFAULT_MAPPER_FIELD,
    models.DateField: DEFAULT_MAPPER_FIELD,
    models.TimeField: DEFAULT_MAPPER_FIELD,
    models.BooleanField: DEFAULT_MAPPER_FIELD,
    models.FileField: DjangoFileField,
}


def create_model_mapper(model_class, model_fields=None, model_exclude=None,
                        model_mapper_fields=None):
    class _mapper_class(ModelMapper):
        class Meta:
            model = model_class
            fields = model_fields
            exclude = model_exclude
            mapper_fields = model_mapper_fields
    return _mapper_class


class ModelMapperMetaclass(BaseMapper):
    def __new__(cls, name, bases, attrs):
        if '_meta' not in attrs:
            opt = Options()
            attrs['_meta'] = opt
        else:
            opt = attrs['_meta']
        # BaseMapperの処理が後に来るので
        # ここで先にoptを拡張する
        mapper_meta = attrs.get('Meta')
        if mapper_meta is not None:
            model = getattr(mapper_meta, 'model', None)
            # Meta.mapper_fields
            mapper_fields = getattr(mapper_meta, 'mapper_fields', None)
            defined_fields = DEFINED_MODEL_MAPPER_FIELDS.copy()
            if mapper_fields:
                defined_fields.update(mapper_fields)
            # Meta.modelが無い場合はエラー
            if model is None:
                raise MetaModelError
            for model_field in model._meta.fields + model._meta.many_to_many:
                # Meta.fields
                if hasattr(mapper_meta, 'fields'):
                    if mapper_meta.fields is not None \
                            and model_field.name not in mapper_meta.fields:
                        continue
                # Meta.exclude
                if hasattr(mapper_meta, 'exclude'):
                    if mapper_meta.exclude is not None \
                            and model_field.name in mapper_meta.exclude:
                        continue
                # モデルのフィールドに対応したField追加
                if model_field.remote_field:
                    # 同じモデルを参照しようとした場合はスキップする
                    if model == model_field.remote_field.model:
                        continue
                    if isinstance(model_field, models.ForeignKey):
                        # ForeignKey
                        related_model_mapper = create_model_mapper(
                            model_field.remote_field.model,
                            model_mapper_fields=mapper_fields)
                        opt.add_field(
                            model_field.name,
                            DelegateField(
                                related_model_mapper,
                                key=model_field.name,
                                required=not model_field.null))
                    elif isinstance(model_field, models.ManyToManyField):
                        # ManyToManyField
                        related_model_mapper = create_model_mapper(
                            model_field.remote_field.model,
                            model_mapper_fields=mapper_fields)
                        opt.add_field(
                            model_field.name,
                            ListDelegateField(
                                related_model_mapper,
                                key=model_field.name,
                                filter=lambda manager: manager.all()))
                else:
                    for defined_field in defined_fields:
                        if isinstance(model_field, defined_field):
                            mapper_field = defined_fields[defined_field]
                            opt.add_field(
                                model_field.name,
                                mapper_field(key=model_field.name))
                            break
                    else:
                        # If there is no match field, use default.
                        opt.add_field(
                            model_field.name,
                            DEFAULT_MAPPER_FIELD(key=model_field.name))
        attrs['_meta'] = opt
        return BaseMapper.__new__(cls, name, bases, attrs)


class ModelMapper(six.with_metaclass(ModelMapperMetaclass, Mapper)):
    """
    Mapper class for Django ORM.

    This class generates mapping definition with using Django Model's Meta
     data.
    """

    def _getattr(self, obj, key):
        """
        Hooks attribute access.
        """
        # If access the empty FK value, return None.
        try:
            return super(ModelMapper, self)._getattr(obj, key)
        except ObjectDoesNotExist:
            return None
