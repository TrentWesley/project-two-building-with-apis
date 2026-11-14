"""
Django settings for the reading list project.

Secret and environment-specific values come from environment variables:
- DJANGO_SECRET_KEY: required when DEBUG is off
- DJANGO_DEBUG: "True" (default) or "False"
- DJANGO_ALLOWED_HOSTS: comma-separated host names (default: localhost,127.0.0.1)
"""

import os
from pathlib import Path

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# A clearly fake key that is only acceptable for local development.
DEV_SECRET_KEY = "dev-only-insecure-key-do-not-use-in-production"

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", DEV_SECRET_KEY)

# Safety check: production (DEBUG off) must never use the fake development key.
if not DEBUG and SECRET_KEY == DEV_SECRET_KEY:
    raise ImproperlyConfigured(
        "Set the DJANGO_SECRET_KEY environment variable when DJANGO_DEBUG is False."
    )

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "books",
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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database: SQLite (the file is gitignored)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Authentication redirects

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "books:list"
LOGOUT_REDIRECT_URL = "home"


# Messages: use Bootstrap's "danger" color for error messages
MESSAGE_TAGS = {messages.ERROR: "danger"}


# Internationalization

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"


# Email (printed to the console; not used by this project)

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
