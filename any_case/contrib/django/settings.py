import importlib
from typing import Any

import django.conf
from django.http import HttpRequest

DEFAULTS = {
    'HEADER_KEY': None,
    'QUERY_KEY': 'case',
    'BODY_KEY': 'case',
    'JSON_MODULE': 'json',
    'CONVERT_INPUT_JSON': True,
    'DUMPS_INPUT_JSON': True,
    'DUMPS_AS_NAME': 'json'
}

IMPORT_MODULES = ['JSON_MODULE']

__all__ = ['django_setting']


class AnyCaseSettings:
    def __init__(self, settings: dict = None, defaults: dict = None) -> None:
        self._defaults = (defaults or DEFAULTS).copy()
        self._settings = {**self._defaults, **settings.copy()}
        self._setup()

    def _setup(self) -> None:
        dumps_name = self._settings['DUMPS_AS_NAME']
        if dumps_name in dir(HttpRequest):
            raise ValueError(
                f"Name {dumps_name!r} clashes with attributes in HttpRequest"
            )

    def __getattr__(self, attr: str) -> Any:
        if attr not in self._defaults:
            raise AttributeError(f'Unknown setting: {attr!r}')

        if attr in IMPORT_MODULES:
            value = importlib.import_module(self._settings[attr])
        else:
            value = self._settings[attr]

        setattr(self, attr, value)
        return value


django_setting = AnyCaseSettings(
    settings=getattr(django.conf.settings, 'ANY_CASE', {}),
    defaults=DEFAULTS,
)
