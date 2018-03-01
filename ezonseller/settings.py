"""
Django settings for ezonseller project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url
#import environ

#env = environ.Env() # set default values and casting
#environ.Env.read_env() # reading .env file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9cejr#ku3=-l0qu+)oz^yj(p(y5v*)3_lo9k6_a9x(vecja$op'


#paypal secret keys
#PAYPAL_MODE = 'live' #or live
#PAYPAL_CLIENT_ID = 'ARhWn4xkBbWb4zdvgLzJ6orUnLtFT0tmbcVY3oINj898G-0Kx9-DVQ5xnukOeY6gi1gZbZ8O2ix2SnLH'
#PAYPAL_CLIENT_SECRECT = 'EM2izzlL_jpky7_6uKoZ2lD0SXdUNfK6zBmkfvYgiEB9x5MwOWFzc9FVrcR8P41aDEgDzsp8XKPNjkyd'
PAYPAL_MODE = 'sandbox' #or live
PAYPAL_CLIENT_ID = 'AaDhiXEsCVKPEhU8I1o4f4z4m0PCKOuGQEyHxzHU9RaDZh_EaUn_3GOf-DhItHyxhtbx1wJKV__0wfAD'
PAYPAL_CLIENT_SECRECT = 'ELjC06xXgQ-vvGRbnPPcjozF39dtbePq7rbSympvyyQdmHlSoOUmDtowXfbOq7QEZ98IL_ErmI24_EqL'

URL = 'https://ezonsellerbackend.herokuapp.com'
#URL = 'http://127.0.0.1:8000'
# SECURITY WARNING: don't run with debug turned on in production!

#if env('DEBUG') == "True":
DEBUG = True
#else:
#    DEBUG = False

ALLOWED_HOSTS = ['ezonseller-backend.herokuapp.com','ezonsellerbackend.herokuapp.com',
                 'localhost', '127.0.0.1:8000', '127.0.0.1', '127.0.0.1:8080',
                 'ezonseller.herokuapp.com', '192.168.0.8',]


# Application definition
DJANGO_APPS = [
  'jet.dashboard',
  'jet',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
]

LOCAL_APPS =[
    'account',
    'notification',
    'payment',
    'product',
]

THIRD_PARTY_APPS = [
  'rest_framework',
  'rest_framework.authtoken',
  'corsheaders',
  'djcelery',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'ezonseller.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ezonseller.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
"""
DATABASES = {
    'default':env.db()
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ezonseller',
        'USER': 'postgres',
        'PASSWORD': 'postgres123',
        'HOST': '127.0.0.1',
        'DATABASE_PORT': '5432',
    }
}
#DJ_DATABASE_URL
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

#Email-AppProjecturation
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@stcsolutions.com.ve'
EMAIL_HOST_PASSWORD = 'v<.VY?GA$+2HK'
EMAIL_PORT = 587

#EMAIL_HOST_USER_SUPPORT = 'support@ezonseller.com'
EMAIL_HOST_USER_SUPPORT = 'carlos5_zeta@hotmail.com'
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Django-RESTFRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'DATETIME_FORMAT': "%d-%m-%Y %H:%M:%S",
}

#cache
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

#Django-CORS
CORS_ORIGIN_ALLOW_ALL = False
# CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Access-Control-Allow-Origin',
)
CORS_ORIGIN_WHITELIST = (
     'localhost:8080',
     '127.0.0.1:8080',
     'localhost:3000',
     '127.0.0.1:3000',
     'localhost:3001',
     '127.0.0.1:3001',
     '0.0.0.0:8080',
     'https://ezonseller.herokuapp.com/',
     'https://ezonsellerfrontend.herokuapp.com/',
     'ezonsellerfrontend.herokuapp.com',
     'ezonseller.herokuapp.com',
     'app.ezonseller.com'
     )
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
#JET ADMIN
#JET_DEFAULT_THEME = 'default'

JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]
#Media-Images
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_USER_MODEL = "account.User"

#recaptcha
RECAPTCHA_CAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCHA_PUBLIC_KEY = '6LejRUMUAAAAAEmqctY7MvmGQ3_AAvKcuvYKBU0x'
RECAPTCHA_PRIVATE_KEY = '6LejRUMUAAAAANzCyOu8_DAc-Rl7BpXRCfKxyvek'


"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/logs.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file'],  # Quiet by default!
            'propagate': False,
            'level': 'ERROR',
        },
    },
}
"""
#celery
#CELERY_BROKER_URL = 'amqp://localhost'
#CELERY_BROKER_URL = 'redis://localhost:6379/0'
#rediscloud
#BROKER_URL = os.environ.get("REDISCLOUD_URL", "django://")
#BROKER_TRANSPORT_OPTIONS = {
#    "max_connections": 2,
#}
#BROKER_POOL_LIMIT = None
#rabbitmqcloud
BROKER_URL = os.environ.get("CLOUDAMQP_URL", "django://")
BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_MAX_RETRIES = None
BROKER_HEARTBEAT  = None # We're using TCP keep-alive instead
RESULT_BACKEND  = None # AMQP is not recommended as result backend as it creates thousands of queues
EVENT_QUEUE_EXPIRES = 60 # Will delete all celeryev. queues without consumers after 1 minute.
WORKER_PREFETCH_MULTIPLIER = 1 # Disable prefetching, it's causes problems and doesn't help performance
WORKER_CONCURRENCY = 50 
#if BROKER_URL == "django://":
#    INSTALLED_APPS += ("kombu.transport.django",) this no work in heroku
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

#CELERY_BROKER_URL = os.environ['REDIS_URL']
#CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
#CELERY_ACCEPT_CONTENT = ['application/json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_TIMEZONE = TIME_ZONE

import djcelery
djcelery.setup_loader()

