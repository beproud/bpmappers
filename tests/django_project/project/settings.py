SECRET_KEY = 'dummy'
DEBUG = True
INSTALLED_APPS = [
    'django_app',
]
MIDDLEWARE = []
ROOT_URLCONF = 'project.urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
