try:
    import django  # NOQA
except ImportError:
    LIB_ENABLED_DJANGO = False
else:
    LIB_ENABLED_DJANGO = True


def lower_class_name(obj):
    return obj.__class__.__name__.lower()
