from importlib import reload

import pytest
from django.conf import settings


@pytest.mark.tryfirst
def pytest_configure():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sites',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.admin.apps.SimpleAdminConfig',
            'django.contrib.staticfiles',
        ],
        ROOT_URLCONF='',
        MIDDLEWARE=[
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        TEMPLATES=[
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
        ],
        DEBUG=True,
    )


@pytest.fixture
def reload_settings():
    import any_case.contrib.django.parser as any_case_parser
    import any_case.contrib.django.settings as any_case_settings

    def wrapper():
        reload(any_case_settings)
        reload(any_case_parser)

    return wrapper
