import importlib
from typing import Any

import django.conf
from django.utils.functional import SimpleLazyObject

DEFAULTS = {
    'HEADER_KEY': 'Accept-Json-Case',
    'QUERY_KEY': None,
    'BODY_KEY': None,
    'JSON_MODULE': 'json',
    'CONVERT_INPUT_JSON': True
}

IMPORT_MODULES = ['JSON_MODULE']

__all__ = ['django_setting']


class AnyCaseSettings:
    def __init__(self, settings: dict = None, defaults: dict = None) -> None:
        self._defaults = (defaults or DEFAULTS).copy()
        self._settings = {**self._defaults, **settings.copy()}

    def __getattr__(self, attr: str) -> Any:
        if attr not in self._defaults:
            raise AttributeError(f'Unknown setting: {attr!r}')

        if attr in IMPORT_MODULES:
            value = importlib.import_module(self._settings[attr])
        else:
            value = self._settings[attr]

        setattr(self, attr, value)
        return value

    @property
    def has_convert_key(self) -> bool:
        return any([self.HEADER_KEY, self.QUERY_KEY, self.BODY_KEY])


django_setting = SimpleLazyObject(
    lambda: AnyCaseSettings(
        settings=getattr(django.conf.settings, 'ANY_CASE', {}),
        defaults=DEFAULTS,
    )
)
