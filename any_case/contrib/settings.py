from typing import Any

import django.conf

DEFAULTS = {
    'HEADER_KEY': None,
    'QUERY_KEY': None,
    'BODY_KEY': None,
}

__all__ = ['django_setting']


class AnyCaseSettings:
    def __init__(self, settings: dict = None, defaults: dict = None) -> None:
        self._defaults = (defaults or DEFAULTS).copy()
        self._settings = {**self._defaults, **settings.copy()}

    def __getattr__(self, attr: str) -> Any:
        if attr not in self._defaults:
            raise AttributeError(f'Unknown setting: {attr!r}')

        return self._settings[attr]


django_setting = AnyCaseSettings(
    settings=getattr(django.conf.settings, 'ANY_CASE', {}),
    defaults=DEFAULTS,
)
