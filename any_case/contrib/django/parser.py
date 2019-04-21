from functools import partial
from typing import Optional

from django.http import HttpRequest

from .settings import django_settings, AnyCaseSettings
from .utils import json_loads, is_json_possible
from ..parser import CaseFormatParser


def parse_header(key: str, request: HttpRequest) -> Optional[str]:
    return request.headers.get(key)


def parse_query(key: str, request: HttpRequest) -> Optional[str]:
    return request.GET.get(key) or request.POST.get(key)


def parse_body(key: str, request: HttpRequest) -> Optional[str]:
    if is_json_possible(request):
        try:
            return json_loads(request).get(key)
        except ValueError:
            pass


def django_case_format_parser(settings: AnyCaseSettings) -> CaseFormatParser:
    parsers = []

    if settings.HEADER_KEY is not None:
        parsers.append(partial(parse_header, settings.HEADER_KEY))
    if settings.QUERY_KEY is not None:
        parsers.append(partial(parse_query, settings.QUERY_KEY))
    if settings.BODY_KEY is not None:
        parsers.append(partial(parse_body, settings.BODY_KEY))

    return CaseFormatParser(parsers)


case_format_parser = django_case_format_parser(django_settings)
