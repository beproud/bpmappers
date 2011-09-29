# vim:fileencoding=utf-8
import unittest

from bpmappers import *

# model
class Person(object):
    def __init__(self, name, val, **extra):
        self.name = name
        self.val = val
        self.__dict__.update(extra)

class Book(object):
    def __init__(self, title, author):
        self.title = title
        self.author = author

# mapper
class PersonMapper(Mapper):
    nick = RawField('name')
    point = RawField('val')

class PersonInherit1(PersonMapper):
    name = RawField()

class PersonInherit2(PersonInherit1):
    foo = RawField('foo')

class PersonInherit3(PersonMapper):
    xxx = NonKeyField()

    def filter_xxx(self):
        return self.options['foo']

class PersonMapper2(Mapper):
    nick = NonKeyField()

    def filter_nick(self):
        return self.options['author_name']

# mapper
class PersonMapper(Mapper):
    nick = RawField('name')
    point = RawField('val')

class BookMapper(Mapper):
    title = RawField()
    author = DelegateField(PersonMapper)

class BookMapper2(Mapper):
    title = RawField()
    author = DelegateField(PersonInherit3)

class BookMapper3(Mapper):
    title = NonKeyField()
    author = NonKeyDelegateField(PersonMapper)

    def filter_title(self):
        return 'moriyoshi_book'

    def filter_author(self):
        return {'name': 'moriyoshi', 'val': 100}

class BookMapper4(Mapper):
    title = RawField()
    author = DelegateField(PersonMapper, after_callback=lambda v: {'author_wrap': v})

class BookMapper5(Mapper):
    title = RawField(callback=lambda v: 'my_%s' % v)
    author = DelegateField(PersonMapper)

    def after_filter_title(self, value):
        return 'wozo_%s' % value

class BookMapper6(Mapper):
    title = RawField()
    author = DelegateField(PersonMapper, required=False)

class BookMapper7(Mapper):
    title = RawField()
    author = DelegateField(PersonMapper2)

class BookFlattenMapper(Mapper):
    title = RawField()
    author = DelegateField(PersonMapper, attach_parent=True)

class ReverseAuthorBookMapper(BookMapper):

    def reverse_name(author):
        author.name = ''.join(reversed(author.name))
        return author

    author = DelegateField(PersonMapper, callback=reverse_name)

class GroupMapper(Mapper):
    name = RawField()
    users = ListDelegateField(PersonMapper)

class GroupMapper2(Mapper):
    name = NonKeyField()
    users = NonKeyListDelegateField(PersonMapper)

    def filter_name(self):
        return self.options.get('name')

    def filter_users(self):
        return [{'name': 'wozozo', 'val': 200}, {'name': 'moriyoshi', 'val': 100}]

class FilteredGroupMapper(GroupMapper):
    users = ListDelegateField(PersonMapper, filter=lambda lst:[p for p in lst if p.val > 10])

class FilteredGroupExMapper(GroupMapper):
    users = ListDelegateField(PersonMapper)

    def filter_users(self, lst):
        return [p for p in lst if p.val > self.options['limit']]

class KeyNameConvertMapper(Mapper):
    name = RawField()

    def key_name(self, name,  value, field):
        return 'ns:%s' % name

# testcase
class FieldsTestCase(unittest.TestCase):
    def test_raw_field(self):
        """
        RawField
        """
        f = RawField('name')
        self.assertEqual(f.get_value(None, 123), 123)
        self.assertEqual(f.get_value(None, 'foo'), 'foo')

    def test_raw_field_callback(self):
        """
        RawField with callback
        """
        f = RawField('name', callback=lambda x:x * x)
        self.assertEqual(f.get_value(None, 10), 100)

    def test_choice_field(self):
        """
        ChoiceField
        """
        f = ChoiceField(['feiz', 'ian'])
        self.assertEqual(f.as_value(None, 0), 'feiz')
        self.assertEqual(f.as_value(None, 1), 'ian')

    def test_stub_field(self):
        """
        StubField
        """
        f = StubField('wozozo')
        self.assertEqual(f.as_value(None), 'wozozo')

class MappersTestCase(unittest.TestCase):

    def setUp(self):
        self.wozozo = Person('wozozo', 10, foo='bar')
        self.moriyoshi = Person('moriyoshi', 20)
        self.ian = Person('ian', 15)
        self.feiz = Person('feiz', -20)
        self.wozo_book = Book('wozo_book', self.wozozo)

    def test_simple_mapper(self):
        """
        Mapper
        """
        mapper = PersonMapper(self.wozozo)
        self.assertEqual(
            mapper.as_dict(),
            {
                'nick': self.wozozo.name,
                'point': self.wozozo.val
            }
        )

    def test_delegate(self):
        """
        DelegateField
        """
        mapper = BookMapper(self.wozo_book)
        self.assertEqual(
            mapper.as_dict(),
            {
                'title': self.wozo_book.title,
                'author': {
                     'nick': self.wozozo.name,
                     'point': self.wozozo.val
                 }
            })

    def test_delegate_callback(self):
        """
        DelegateField with callback
        and class inheritance
        """
        mapper = ReverseAuthorBookMapper(self.wozo_book)
        self.assertEqual(
            mapper.as_dict(),
            {
                'title': self.wozo_book.title,
                'author': {
                     'nick': 'ozozow',
                     'point': self.wozozo.val
                 }
            })

    def test_delegate_none_value(self):
        """
        when value is None
        """
        book = Book('wozo_book', None)
        mapper = BookMapper6(book)
        self.assertEqual(
            mapper.as_dict(),
            {
                'title': book.title,
                'author': None,
            })

    def test_list_delegate(self):
        """
        ListDelegateField
        """
        mapper = GroupMapper(dict(
            name='beproud',
            users=[self.wozozo, self.moriyoshi]
        ))
        self.assertEqual(
            mapper.as_dict(),
            {
                'name': 'beproud',
                'users': [
                    {'nick': self.wozozo.name, 'point': self.wozozo.val},
                    {'nick': self.moriyoshi.name, 'point': self.moriyoshi.val},
                ]
            })

    def test_list_delegate_filter(self):
        """
        ListDelegateField with filter
        """
        mapper = FilteredGroupMapper(dict(
            name='over10',
            users=[
                self.wozozo,
                self.moriyoshi,
                self.ian,
                self.feiz,
            ]))
        self.assertEqual(
            mapper.as_dict(),
            {
                'name': 'over10',
                'users': [
                    {'nick': self.moriyoshi.name, 'point': self.moriyoshi.val},
                    {'nick': self.ian.name, 'point': self.ian.val},
                ]
            })

    def test_list_delegate_filter_method(self):
        """
        ListDelegateField with filter method
        """
        mapper = FilteredGroupExMapper(dict(
            name='over10',
            users=[
                self.wozozo,
                self.moriyoshi,
                self.ian,
                self.feiz,
            ]),
            limit=10)
        self.assertEqual(
            mapper.as_dict(),
            {
                'name': 'over10',
                'users': [
                    {'nick': self.moriyoshi.name, 'point': self.moriyoshi.val},
                    {'nick': self.ian.name, 'point': self.ian.val},
                ]
            })

    def test_inheritance(self):
        """
        継承のテスト
        """
        mapper = PersonInherit2(self.wozozo)
        self.assertEqual(
            mapper.as_dict(),
            {
                'nick': self.wozozo.name,
                'point': self.wozozo.val,
                'name': self.wozozo.name,
                'foo': self.wozozo.foo,
            }
        )

    def test_list_data(self):
        """
        dataパラメータがリストの場合
        """
        mapper = PersonInherit2([self.moriyoshi, {'foo': 'bar'}])
        self.assertEqual(
            mapper.as_dict(),
            {
                'nick': self.moriyoshi.name,
                'point': self.moriyoshi.val,
                'name': self.moriyoshi.name,
                'foo': 'bar',
            }
        )

    def test_options_and_non_key_field(self):
        """
        mapper options and non key field
        """
        mapper = BookMapper2(self.wozo_book, foo='foo')
        self.assertEqual(
            mapper.as_dict(),
            {
                'title': self.wozo_book.title,
                'author': {
                     'nick': self.wozozo.name,
                     'point': self.wozozo.val,
                     'xxx': 'foo'
                 }
            })

    def test_options_and_delegate_field(self):
        """
        mapper options and delegate field
        """
        mapper = BookMapper7(self.wozo_book, author_name='moriyoshi')
        self.assertEqual(
            mapper.as_dict(),
            {
                'title': self.wozo_book.title,
                'author': {
                    'nick': 'moriyoshi',
                }
            })

    def test_non_key_delegate(self):
        """
        mapper non key delegate field
        """
        mapper = BookMapper3()
        self.assertEqual(
            mapper.as_dict(),
            {
                'title': 'moriyoshi_book',
                'author': {
                     'nick': 'moriyoshi',
                     'point': 100,
                 }
            })

    def test_delegate_field_attach_parent(self):
        """
        attach_parent delegate field 
        """
        mapper = BookFlattenMapper(self.wozo_book)
        self.assertEqual(
            mapper.as_dict(),
            {
                'title': 'wozo_book',
                'nick': 'wozozo',
                'point': 10,
            })

    def test_non_key_list_delegate(self):
        """
        mapper non key list delegate field
        """
        mapper = GroupMapper2(name='foo')
        self.assertEqual(
            mapper.as_dict(),
            {
                'name': 'foo',
                'users': [
                    {
                     'nick': 'wozozo',
                     'point': 200,
                    },
                    {
                     'nick': 'moriyoshi',
                     'point': 100,
                    },
                ]
            })

    def test_after_callback(self):
        mapper = BookMapper4(self.wozo_book)
        self.assertEqual(
            mapper.as_dict(),
            {
                'title': self.wozo_book.title,
                'author': {
                    'author_wrap': {
                        'nick': self.wozozo.name,
                        'point': self.wozozo.val,
                    }
                }
            })

    def test_after_filter_method(self):
        mapper = BookMapper5(self.wozo_book)
        self.assertEqual(
            mapper.as_dict(),
            {
                'title': 'wozo_my_%s' % self.wozo_book.title,
                'author': {
                    'nick': self.wozozo.name,
                    'point': self.wozozo.val,
                }
            })

    def test_key_name_convert(self):
        mapper = KeyNameConvertMapper(self.wozozo)
        self.assertEqual(
            mapper.as_dict(),
            {
                'ns:name': self.wozozo.name,
            })


# djangomodel mapper
"""
Standalone django model test with a 'memory-only-django-installation'.
You can play with a django model without a complete django app installation.
http://www.djangosnippets.org/snippets/1044/
"""

import os

APP_LABEL = os.path.splitext(os.path.basename(__file__))[0]

import django
os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
from django.conf import global_settings

global_settings.INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #APP_LABEL,
)
if django.VERSION > (1, 3):
    global_settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
else:
    global_settings.DATABASE_ENGINE = "sqlite3"
    global_settings.DATABASE_NAME = ":memory:"

from django.core.management import sql

from django.core.management.color import no_style
STYLE = no_style()

def create_table(*models):
    """ Create all tables for the given models """
    from django.db import connection
    cursor = connection.cursor()
    def execute(statements):
        for statement in statements:
            try:
                cursor.execute(statement)
            except:
                pass

    for model in models:
        execute(connection.creation.sql_create_model(model, STYLE)[0])
        execute(connection.creation.sql_for_many_to_many(model, STYLE))
#______________________________________________________________________________
# Your test model classes:
import django
from django.db import models

from bpmappers.djangomodel import *

# djangomodel
class PersonModel(models.Model):
    name = models.CharField(max_length=10)
    val = models.IntegerField()

    class Meta:
        app_label = APP_LABEL

class BookModel(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(PersonModel)

    class Meta:
        app_label = APP_LABEL

class TagModel(models.Model):
    label = models.CharField(max_length=20)

    class Meta:
        app_label = APP_LABEL

class TaggedItemModel(models.Model):
    name = models.CharField(max_length=20)
    tags = models.ManyToManyField(TagModel, blank=True, auto_created=True)

    class Meta:
        app_label = APP_LABEL

class PersonExModel(PersonModel):
    spam = models.CharField(max_length=10)

    class Meta:
        app_label = APP_LABEL

class FlagModel(models.Model):
    flg = models.BooleanField()

    class Meta:
        app_label = APP_LABEL

class RecursionModel(models.Model):
    recursion = models.ForeignKey('RecursionModel')

    class Meta:
        app_label = APP_LABEL

class DateAndTimeModel(models.Model):
    start_date = models.DateField()
    start_time = models.TimeField()

    class Meta:
        app_label = APP_LABEL

class MyField(models.Field):
    pass

class UnknownFieldModel(models.Model):
    myfield = MyField(max_length=20)

    class Meta:
        app_label = APP_LABEL

class FileFieldModel(models.Model):
    myfile = models.FileField(upload_to='./')
    myimage = models.ImageField(upload_to='./')

    class Meta:
        app_label = APP_LABEL

class FreePersonGroupModel(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        app_label = APP_LABEL

class FreePersonModel(models.Model):
    name = models.CharField(max_length=20)
    group = models.ForeignKey(FreePersonGroupModel, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL

#djangomodelmapper
class PersonModelMapper(ModelMapper):
    class Meta:
        model = PersonModel
        exclude = ['id']

class PersonExModelMapper(ModelMapper):
    class Meta:
        model = PersonExModel
        fields = ['id', 'name', 'spam']

class InheritModelMapper1(PersonModelMapper):
    foo = RawField()

    class Meta(PersonModelMapper.Meta):
        pass

class BookModelMapper(ModelMapper):
    class Meta:
        model = BookModel

class BookModelMapper2(ModelMapper):
    author = DelegateField(PersonModelMapper, required=False)

    class Meta:
        model = BookModel

class BookModelExMapper(ModelMapper):
    author = DelegateField(PersonExModelMapper)

    class Meta:
        model = BookModel

class GroupModelMapper(Mapper):
    name = RawField()
    users = ListDelegateField(PersonModelMapper)

class TaggedItemModelMapper(ModelMapper):
    class Meta:
        model = TaggedItemModel

class FlagModelMapper(ModelMapper):
    class Meta:
        model = FlagModel

class DateAndTimeModelMapper(ModelMapper):
    class Meta:
        model = DateAndTimeModel

class UnknownFieldModelMapper(ModelMapper):
    class Meta:
        model = UnknownFieldModel

class BookModelExFlattenMapper(BookModelExMapper):
    author = DelegateField(PersonExModelMapper)

    class Meta(BookModelExMapper.Meta):
        pass

    def attach_author(self, parsed, value):
        parsed.update(value)

class FileFieldModelMapper(ModelMapper):
    class Meta:
        model = FileFieldModel

class KeyNameConvertModelMapper(ModelMapper):
    def key_name(self, name, value, field):
        return 'prefix:%s' % name

    class Meta:
        model = PersonModel

class FreePersonGroupModelMapper(ModelMapper):
    class Meta:
        model = FreePersonGroupModel

class FreePersonModelMapper(ModelMapper):
    group = DelegateField(FreePersonGroupModelMapper)

    class Meta:
        model = FreePersonModel

# djangomodelmapper test
class DjangoModelMappersTestCase(unittest.TestCase):

    def setUp(self):
        import sys
        sys.modules['tests.models'] = None
        from django.core import management
        management.call_command('syncdb', verbosity=1, interactive=False)

        create_table(TagModel, TaggedItemModel)

        self.wozozo = PersonModel(id=1, name='wozozo', val=10)
        self.moriyoshi = PersonModel(id=2, name='wozozo', val=20)
        self.wozozo_ex = PersonExModel(id=3, name='wozozo_ex', val=100, spam='egg')
        self.wozo_book = BookModel(id=1, title='wozo_book', author=self.wozozo)
        self.wozo_book_ex = BookModel(id=1, title='wozo_book', author=self.wozozo_ex)
        self.tag_skype = TagModel(id=1, label='skype')
        self.tag_skype.save()
        self.tag_redbull = TagModel(id=2, label='redbull')
        self.tag_redbull.save()
        self.tagged_item = TaggedItemModel(id=1, name='bpbot')
        self.flag_wozozo = FlagModel(id=1, flg=True)
        self.flag_moriyoshi = FlagModel(id=2, flg=False)
        self.wozo_free = FreePersonModel(id=1, name='wozozo')
  
        self.tagged_item.save()
        self.tagged_item.tags.add(self.tag_skype)
        self.tagged_item.tags.add(self.tag_redbull)

    def test_simple_model_mapper(self):
        mapper = PersonModelMapper(self.wozozo)
        self.assertEqual(
            mapper.as_dict(),
            {
                'name': self.wozozo.name,
                'val': self.wozozo.val
            }
        )

    def test_inherit(self):
        """
        Inherit
        """
        mapper = InheritModelMapper1([self.wozozo, {'foo': 'bar'}])
        self.assertEqual(
            mapper.as_dict(),
            {
                'name': self.wozozo.name,
                'val': self.wozozo.val,
                'foo': 'bar'
            }
        )

    def test_list_delegate(self):
        """
        ListDelegateField
        """
        mapper = GroupModelMapper(dict(
            name='bpmodel',
            users=[
                self.wozozo,
                self.moriyoshi
            ]))
        self.assertEqual(
            mapper.as_dict(),
            {
                'name': 'bpmodel',
                'users': [
                    {
                        'name': self.wozozo.name,
                        'val': self.wozozo.val
                    },
                    {
                        'name': self.moriyoshi.name,
                        'val': self.moriyoshi.val
                    }
                ]
            }
        )

    def test_model_inherit_meta_fields(self):
        """
        Model inheritance
        and Meta.fields
        """
        mapper = PersonExModelMapper(self.wozozo_ex)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': self.wozozo_ex.id,
                'name': self.wozozo_ex.name,
                'spam': self.wozozo_ex.spam,
            }
        )

    def test_related_foreign_key(self):
        """
        ForeignKey
        """
        mapper = BookModelMapper(self.wozo_book)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': self.wozo_book.id,
                'title': self.wozo_book.title,
                'author': {
                    'id': self.wozozo.id,
                    'name': self.wozozo.name,
                    'val': self.wozozo.val
                }
            }
        )

    def test_related_none_value(self):
        """
        when value is None
        """
        book = BookModel(id=1, title='wozo_book')
        mapper = BookModelMapper2(book)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': book.id,
                'title': book.title,
                'author': None,
            })

    def test_model_mapper_custom_field(self):
        """
        ModelMapper custom field
        """
        mapper = BookModelExMapper(self.wozo_book_ex)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': self.wozo_book.id,
                'title': self.wozo_book.title,
                'author': {
                    'id': self.wozozo_ex.id,
                    'name': self.wozozo_ex.name,
                    'spam': self.wozozo_ex.spam,
                }
            }
        )

    def test_related_many_to_many(self):
        """
        ManyToManyField
        """
        mapper = TaggedItemModelMapper(self.tagged_item)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': self.tagged_item.id,
                'name': self.tagged_item.name,
                'tags': [
                    {
                        'id': self.tag_skype.id,
                        'label': self.tag_skype.label,
                    },
                    {
                        'id': self.tag_redbull.id,
                        'label': self.tag_redbull.label,
                    },
                ]
            }
        )

    def test_create_model_mapper(self):
        """
        create_model_mapper
        """
        mapper = create_model_mapper(PersonModel, model_fields=['id', 'name'])(self.wozozo)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': self.wozozo.id,
                'name': self.wozozo.name,
            }
        )

    def test_flag_model_mapper(self):
        """
        BooleanField
        """
        mapper = FlagModelMapper(self.flag_wozozo)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': self.flag_wozozo.id,
                'flg': self.flag_wozozo.flg,
            }
        )
        mapper = FlagModelMapper(self.flag_moriyoshi)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': self.flag_moriyoshi.id,
                'flg': self.flag_moriyoshi.flg,
            }
        )

    def test_create_recursion_model_mapper(self):
        """
        create recursion relation model
        """
        class RecursionModelMapper(ModelMapper):
            class Meta:
                model = RecursionModel
        mapper = RecursionModelMapper(RecursionModel(id=1))
        self.assertEqual(mapper.as_dict(), {'id': 1})

    def test_date_and_time_model_mapper(self):
        """
        date and time field model
        """
        import datetime
        obj = DateAndTimeModel(id=1, start_date=datetime.date(2020, 4, 1), start_time=datetime.time(10, 10))
        mapper = DateAndTimeModelMapper(obj)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': 1,
                'start_date': datetime.date(2020, 4, 1),
                'start_time': datetime.time(10, 10),
            }
        )

    def test_unknown_field_model_mapper(self):
        """
        unknown field model
        """
        obj = UnknownFieldModel(id=1, myfield = 'unknown')
        mapper = UnknownFieldModelMapper(obj)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': 1,
                'myfield': 'unknown',
            }
        )

    def test_flatten_delegate_mapper(self):
        """
        flatten delegate field
        """
        mapper = BookModelExFlattenMapper(self.wozo_book_ex)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': self.wozozo_ex.id,
                'title': self.wozo_book.title,
                'name': self.wozozo_ex.name,
                'spam': self.wozozo_ex.spam,
            }
        )

    def test_file_field_mapper(self):
        """
        FileField
        """
        obj = FileFieldModel()
        obj.pk = 1
        # django 1.0.x is not able to set name attribute.
        if django.VERSION < (1, 1):
            print "hogehogehoge"
            obj.myfile._name = 'test.dat'
            obj.myimage._name = 'image.dat'
        else:
            obj.myfile.name = 'test.dat'
            obj.myimage.name = 'image.dat'
        mapper = FileFieldModelMapper(obj)
        self.assertEqual(
            mapper.as_dict(),
            {
                'id': 1,
                'myfile': 'test.dat',
                'myimage': 'image.dat',
            }
        )

    def test_key_name_convert_model_mapper(self):
        mapper = KeyNameConvertModelMapper(self.wozozo)
        self.assertEqual(
            mapper.as_dict(),
            {
                'prefix:id': self.wozozo.id,
                'prefix:name': self.wozozo.name,
                'prefix:val': self.wozozo.val
            }
        )

    def test_fk_none_fail_model_mapper(self):
        mapper = FreePersonModelMapper(self.wozo_free)
        self.assertRaises(InvalidDelegateException, mapper.as_dict)


if __name__ == '__main__':
    unittest.main()
