"""
Django settings for pizzeria_project.

UWAGA: Ten projekt celowo NIE używa Django ORM (modeli/migracji/bazy danych).
Dane są przechowywane w plikach JSON za pomocą rozwiazanie_weekend2/.
DATABASES = {} (puste) - nie ma bazy danych ani warningów o migracjach.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-pizzeria-workshop-key-not-for-production'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.messages',
    # TODO: Dodaj swoje appy tutaj po uzyciu 'python manage.py startapp <nazwa>'
    # np. 'menu_app',
    # np. 'customers_app',
    # np. 'orders_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pizzeria_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pizzeria_project.wsgi.application'

DATABASES = {}

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Uzywamy cookie storage zamiast domyslnego session storage,
# bo nie mamy session middleware (nie uzywamy bazy danych)
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
