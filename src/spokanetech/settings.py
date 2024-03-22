"""
Django settings for spokanetech project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

IS_DEVELOPMENT = bool(os.environ.get("SPOKANE_TECH_DEV", False))
if IS_DEVELOPMENT:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "django-insecure-t9*!4^fdn*=pmz4%8u_we!88e!8@_!drx0)u_@6$@!nx$4svjp"  # nosec: Development-only key.

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []
else:
    try:
        SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
    except KeyError as e:
        raise KeyError(f"{e}: If running in development, set 'SPOKANE_TECH_DEV' to any value.") from e

    DEBUG = False
    ALLOWED_HOSTS = ["spokanetech.org", "spokanetech-py.fly.dev"]
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

    # SSL Options
    # TODO: These will have to change depending on how infra-platform handles SSL termination
    # https://docs.djangoproject.com/en/5.0/ref/settings/#secure-hsts-preload
    SECURE_HSTS_SECONDS = 0
    SECURE_SSL_REDIRECT = False

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "django_celery_results",
    "django_celery_beat",
    "handyhelpers",
    "web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "spokanetech.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "spokanetech.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:////{BASE_DIR}/db.sqlite3",
        conn_max_age=600,
        conn_health_checks=True,
    ),
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Storages
USE_AZURE = os.environ["USE_AZURE"] == "true" if "USE_AZURE" in os.environ else not DEBUG
if USE_AZURE:
    DEFAULT_FILE_STORAGE = "spokanetech.backend.AzureMediaStorage"
    STATICFILES_STORAGE = "spokanetech.backend.AzureStaticStorage"

    STATIC_LOCATION = "static"
    MEDIA_LOCATION = "media"

    AZURE_URL_EXPIRATION_SECS = None
    AZURE_ACCOUNT_NAME = os.environ["AZURE_ACCOUNT_NAME"]
    AZURE_ACCOUNT_KEY = os.environ["AZURE_ACCOUNT_KEY"]
    AZURE_CUSTOM_DOMAIN = os.environ.get(
        "AZURE_CDN_DOMAIN",
        f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net",
    )
    STATIC_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
    MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/"
    MEDIA_UPLOAD_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}"
else:
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


PROJECT_NAME = "Spokane Tech"
PROJECT_DESCRIPTION = """Community resource for all things tech in the Spokane and CDA area"""
PROJECT_VERSION = "0.0.1"


# Celery
CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "django-db")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_ACKS_LATE = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


# Discord
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
