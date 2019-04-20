from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from any_case import converts_keys
from .parser import case_format_parser
from .settings import django_setting
from .utils import json, json_loads, is_json_possible, is_json_content

__all__ = ['KeysConverterMiddleware']


class KeysConverterMiddleware(MiddlewareMixin):
    if django_setting.CONVERT_INPUT_JSON:

        @staticmethod
        def process_request(request: HttpRequest) -> HttpRequest:
            if is_json_possible(request):
                try:
                    json_body = json_loads(request)
                    converted = converts_keys(
                        json_body, case='snake', inplace=True,
                    )
                    request.json = converted
                except ValueError:
                    pass

            return request

    if django_setting.has_convert_key:
        @staticmethod
        def process_response(
                request: HttpRequest,
                response: HttpResponse,
        ) -> HttpResponse:
            if is_json_content(response):
                try:
                    case = case_format_parser.parse(request, raise_exc=True)
                    json_content = json.loads(response.content)
                    converted = converts_keys(json_content, case=case, inplace=True)
                    response.content = json.dumps(converted)
                except ValueError:
                    pass

            return response
