from path import path

SECRET_KEY = 'SEKRIT'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.admin',
    'coffin',
    'treeadmin',
    'konoha',
    'konoha.tests',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'enumfields.db',
        'TEST_NAME': 'enumfields.db',
    },
}

ROOT_URLCONF = 'konoha.tests.urls'

DEBUG = True

STATIC_URL = "/static/"


KONOHA_DATASOURCES = {
    'test': 'konoha.tests.datasources',
    'repeat': "konoha.tests.datasources.repeat"
}

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.core.context_processors.csrf',
    'konoha.contextprocessors.datasources'
]

KONOHA_TEMPLATES = {
    'Index': "tests/index.html",
    'Content': "tests/content.html",
    'About': "tests/about.html"}


MAX_VERSIONS_NUM = 10
MAX_VERSIONS_PERIOD = 100

KONOHA_ROOT = ''