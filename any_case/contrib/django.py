import json
from typing import Optional

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import cached_property

from .case_parser import CaseFormatParser
from .settings import django_setting
from .. import converts_keys


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
            return json.loads(request.body).get(django_setting.BODY_KEY)
        except ValueError:
            pass


class KeysConverterMiddleware(MiddlewareMixin):
    @cached_property
    def case_format_parser(self) -> CaseFormatParser:
        parsers = []

        if django_setting.HEADER_KEY is not None:
            parsers.append(parse_header)
        if django_setting.QUERY_KEY is not None:
            parsers.append(parse_query)
        if django_setting.BODY_KEY is not None:
            parsers.append(parse_body)

        return CaseFormatParser(parsers)

    @staticmethod
    def process_request(request: HttpRequest) -> HttpRequest:
        if request.content_type == 'application/json':

            try:
                json_body = json.loads(request.body)
                converted = converts_keys(json_body, case='snake')
                request._body = json.dumps(converted)
            except ValueError:
                pass

        return request

    def process_response(
            self,
            request: HttpRequest,
            response: HttpResponse,
    ) -> HttpResponse:
        if response.get('Content-Type') == 'application/json':

            try:
                case = self.case_format_parser.parse(request)
                json_content = json.loads(response.content)
                converted = converts_keys(json_content, case=case)
                response.content = json.dumps(converted)
            except ValueError:
                pass

        return response
