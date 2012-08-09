from .testing import TestCase

from bpmappers import exceptions


class DataErrorTest(TestCase):
    def test_get_value(self):
        err = exceptions.DataError("spam")
        self.assertEqual(str(err), "'spam'")
