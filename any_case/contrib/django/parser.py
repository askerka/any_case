from typing import Optional

from django.http import HttpRequest

from .settings import django_settings
from .utils import json_loads, is_json_possible
from ..parser import CaseFormatParser


def parse_header(request: HttpRequest) -> Optional[str]:
    return request.headers.get(django_settings.HEADER_KEY)


def parse_query(request: HttpRequest) -> Optional[str]:
    return (
            request.GET.get(django_settings.QUERY_KEY) or
            request.POST.get(django_settings.QUERY_KEY)
    )


def parse_body(request: HttpRequest) -> Optional[str]:
    if is_json_possible(request):
        try:
            return json_loads(request).get(django_settings.BODY_KEY)
        except ValueError:
            pass


def django_case_format_parser() -> CaseFormatParser:
    parsers = []

    if django_settings.HEADER_KEY is not None:
        parsers.append(parse_header)
    if django_settings.QUERY_KEY is not None:
        parsers.append(parse_query)
    if django_settings.BODY_KEY is not None:
        parsers.append(parse_body)

    return CaseFormatParser(parsers)


case_format_parser = django_case_format_parser()
