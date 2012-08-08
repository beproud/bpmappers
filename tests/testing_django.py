try:
    import django
except ImportError:
    LIB_ENABLED_DJANGO = False
else:
    LIB_ENABLED_DJANGO = True


def initialize():
    from django.conf import settings
    settings.configure()


def _setup_db():
    pass


def _teardown_db():
    pass
