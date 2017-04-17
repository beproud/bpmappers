class TestDataError:
    def test_get_value(self):
        from bpmappers import exceptions
        err = exceptions.DataError("spam")
        assert str(err) == "'spam'"
