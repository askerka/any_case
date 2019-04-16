from typing import Union, Any

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from any_case import converts_keys
from .parser import case_format_parser
from .settings import django_setting
from .utils import json, json_loads

__all__ = ['KeysConverterMiddleware']


class KeysConverterMiddleware(MiddlewareMixin):
    if django_setting.CONVERT_INPUT_JSON:

        def process_request(self, request: HttpRequest) -> HttpRequest:
            if request.content_type == 'application/json':
                try:
                    json_body = json_loads(request)
                    converted = converts_keys(
                        json_body, case='snake', inplace=True,
                    )
                    self.dumps_json(request, converted)
                except ValueError:
                    pass

            return request

        if not django_setting.DUMPS_INPUT_JSON:
            @staticmethod
            def dumps_json(request: HttpRequest, result: Any) -> None:
                pass

        elif django_setting.DUMPS_AS_NAME == 'body':
            @staticmethod
            def dumps_json(request: HttpRequest, result: Any) -> None:
                request._body = result

        else:
            @staticmethod
            def dumps_json(request: HttpRequest, result: Any) -> None:
                setattr(request, django_setting.DUMPS_AS_NAME, result)

    @staticmethod
    def process_response(
            request: HttpRequest,
            response: HttpResponse,
    ) -> HttpResponse:
        if response.get('Content-Type') == 'application/json':

            try:
                case = case_format_parser.parse(request)
                json_content = json.loads(response.content)
                converted = converts_keys(json_content, case=case, inplace=True)
                response.content = json.dumps(converted)
            except ValueError:
                pass

        return response
