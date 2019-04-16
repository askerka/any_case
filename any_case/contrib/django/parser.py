from typing import Optional

from django.http import HttpRequest

from .settings import django_setting
from .utils import json_loads
from ..parser import CaseFormatParser


def parse_header(request: HttpRequest) -> Optional[str]:
    return request.headers.get(django_setting.HTTP_HEADER_KEY)


def parse_query(request: HttpRequest) -> Optional[str]:
    return (
            request.GET.get(django_setting.QUERY_KEY)
            or request.POST.get(django_setting.QUERY_KEY)
    )


def parse_body(request: HttpRequest) -> Optional[str]:
    if (
            request.method not in {'GET', 'HEAD'}
            and request.content_type == 'application/json'
    ):
        try:
            return json_loads(request).get(django_setting.BODY_KEY)
        except ValueError:
            pass


def django_case_format_parser() -> CaseFormatParser:
    parsers = []

    if django_setting.HEADER_KEY is not None:
        parsers.append(parse_header)
    if django_setting.QUERY_KEY is not None:
        parsers.append(parse_query)
    if django_setting.BODY_KEY is not None:
        parsers.append(parse_body)

    return CaseFormatParser(parsers)


case_format_parser = django_case_format_parser()
