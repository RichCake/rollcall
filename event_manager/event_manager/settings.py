import os
from pathlib import Path

from dotenv import load_dotenv


def str_to_bool(string):
    return string.lower() in ['true', '1', 't', 'y', 'yes']


load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', default='aaa')

DEBUG = str_to_bool(os.getenv('DJANGO_DEBUG', default='false'))

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split(",")

CSRF_TRUSTED_ORIGINS = [
    "5.35.127.251:1337",
]

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'events.apps.EventsConfig',
    'users.apps.UsersConfig',
    'homepage.apps.HomepageConfig',
    'gamestat.apps.GamestatConfig',
    'games.apps.GamesConfig',
    'categories.apps.CategoriesConfig',
    'profiles.apps.ProfilesConfig',
    'crispy_forms',
    'crispy_bootstrap4',
    'django_celery_beat',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

ROOT_URLCONF = 'event_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'event_manager.wsgi.application'

PG_DB_NAME = os.getenv("PG_DB_NAME")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': PG_DB_NAME,
        'USER': PG_USER,
        'PASSWORD': PG_PASSWORD,
        'HOST': 'pgdb',
        'PORT': '5432',
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    },
]


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'


if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['localhost', '127.0.0.1']
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG,
    }


CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MAIL = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = MAIL
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


LOGIN_URL = 'users:login_tg'
LOGIN_REDIRECT_URL = '/'

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_RESULT_EXPIRES = 18000
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

TG_TOKEN = os.getenv('TG_BOT_TOKEN')

# STEAM

STEAM_API_KEY = os.getenv("STEAM_API_KEY")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

SOCIAL_AUTH_JSONFIELD_ENABLED = True

AUTHENTICATION_BACKENDS = [
    'social_core.backends.telegram.TelegramAuth',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = TG_TOKEN

CSRF_TRUSTED_ORIGINS = ["http://localhost:1337"]