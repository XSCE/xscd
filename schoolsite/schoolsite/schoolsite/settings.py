import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Tony', 'tony_anderson@usa.net'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/library/mysql.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': ''
    }
}

TIME_ZONE = None

LANGUAGE_CODE = 'en-us'

USE_I18N = True

STATIC_URL = '/static/'
STATICFILES_DIR = (
    '/library/schoolsite/static/',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=%qrv^l=@j38yqc*1fod*#ubx-#3gkw-l&amp;-p*v6^6#hdv46p*k'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    "/library/schoolsite/templates/",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
'django.middleware.common.CommonMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
)


ROOT_URLCONF = 'schoolsite.urls'

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'library',
    'kls',
)

