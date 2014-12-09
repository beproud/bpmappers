try:
    import django
except ImportError:
    LIB_ENABLED_DJANGO = False
else:
    LIB_ENABLED_DJANGO = True


def lower_class_name(obj):
    return obj.__class__.__name__.lower()


def get_django_version():
    return django.VERSION


def initialize():
    from django.conf import settings
    if get_django_version() >= (1, 2):
        settings_dict = dict(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                },
            },
            MIDDLEWARE_CLASSES=(),
        )
    else:
        settings_dict = dict(
            DEBUG=True,
            DATABASE_ENGINE='sqlite3',
            DATABASE_NAME=':memory:'
        )
    if not settings.configured:
        settings.configure(**settings_dict)

    # In Django 1.7 or later, using "django.apps" module.
    if get_django_version() >= (1, 7):
        from django.apps import apps
        if not apps.ready:
            apps.populate(settings.INSTALLED_APPS)
            from django.core.management import call_command
            call_command('migrate', interactive=False)
    else:
        from django.db.models.loading import cache as model_cache
        if not model_cache.loaded:
            model_cache._populate()
            from django.core.management import call_command
            call_command('syncdb', interactive=False)


def get_connection():
    "get default database connection"
    if get_django_version() >= (1, 2):
        from django.db import connections
        connection = connections['default']
    else:
        from django.db import connection
    return connection


def get_cursor(connection):
    "get database cursor from connection"
    return connection.cursor()


def get_style():
    from django.core.management.color import no_style
    return no_style()


def create_table(model):
    connection = get_connection()
    cursor = get_cursor(connection)
    style = get_style()
    pending_references = {}

    sql, references = connection.creation.sql_create_model(
        model, style)
    for statement in sql:
        cursor.execute(statement)
    for f in model._meta.many_to_many:
        if get_django_version() >= (1, 2):
            create_table(f.rel.through)
        else:
            m2m_sql = connection.creation.sql_for_many_to_many(model, style)
            if m2m_sql:
                cursor.execute(m2m_sql[0])


def _setup_db():
    return get_connection()


def _teardown_db():
    get_connection().close()
