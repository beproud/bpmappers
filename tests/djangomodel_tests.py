import testing_django

from testing import TestCase, SkipTest

models = None
djangomodel = None


def setUpModule():
    if not testing_django.LIB_ENABLED_DJANGO:
        raise SkipTest("Django is not installed.")
    testing_django.initialize()
    # replace models
    global models
    from django.db import models as django_models
    models = django_models
    # replace djangomodel
    global djangomodel
    from bpmappers import djangomodel as bpmappers_djangomodel
    djangomodel = bpmappers_djangomodel


class ModelMapperTest(TestCase):
    def setUp(self):
        class DummyModel(models.Model):
            spam = models.CharField(max_length=30)
            bacon = models.CharField(max_length=30)

            class Meta:
                app_label = "testing"

        self.obj = DummyModel(id=1, spam="egg", bacon="ham")

        class TestMapper(djangomodel.ModelMapper):
            class Meta:
                model = DummyModel

        self.mapper_class = TestMapper

    def test_mapping(self):
        mapper = self.mapper_class(self.obj)
        result = mapper.as_dict()
        self.assertEqual(result, {
            'id': 1,
            'spam': "egg",
            'bacon': "ham",
        })
