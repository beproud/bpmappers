try:
    import django
except ImportError:
    LIB_ENABLED_DJANGO = False
else:
    LIB_ENABLED_DJANGO = True


def lower_class_name(obj):
    return obj.__class__.__name__.lower()


def initialize():
    from django.conf import settings
    settings.configure()


def _setup_db():
    pass


def _teardown_db():
    pass
