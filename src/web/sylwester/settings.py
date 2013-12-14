import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
        ('Piotr Dobrowolski', 'dobrypd@gmiail.com'),
)

ALLOWED_HOSTS = ['sylwesterczarnorzeki.dobrowolski.net.pl', 'groovie', 'dobrowolski.net.pl']

MANAGERS = ADMINS


ALBUMS = ['NewYearSEve02', 'Our18thBirthday', 'ChristmasEveAfterParty']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), '../database.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Warsaw'

LANGUAGE_CODE = 'pl-pl'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = '#MY_STATIC_ROOT_IF_DEBUG##'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), '../static'),
)

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '##DJANGO_SECRET##'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'sylwester.urls'

WSGI_APPLICATION = 'sylwester.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'playlist',
    'django.contrib.admin',
    'social.apps.django_app.default',
    'picasso',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = '##FB_APP_KEY##'
SOCIAL_AUTH_FACEBOOK_SECRET = '##FB_SECRET##'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

LOGIN_ERROR_URL    = "/"

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#PICASSO
PICASSO_USER = 'dobrypd'
PICASSO_THUMBSIZES = ('72c', '160c',)
PICASSO_IMGMAX = '1600'
PICASSO_INDEX_ALBUMS = 3
PICASSO_INDEX_PHOTOS = 9
PICASSO_LATEST_PHOTOS = 15

