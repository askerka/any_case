from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from any_case import converts_keys
from .parser import case_format_parser
from ..settings import django_setting

__all__ = ['KeysConverterMiddleware']


class KeysConverterMiddleware(MiddlewareMixin):
    json = django_setting.JSON_MODULE

    def process_request(self, request: HttpRequest) -> HttpRequest:
        if request.content_type == 'application/json':

            try:
                json_body = self.json.loads(request.body)
                converted = converts_keys(json_body, case='snake', inplace=True)
                request._body = self.json.dumps(converted)
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
                case = case_format_parser.parse(request)
                json_content = self.json.loads(response.content)
                converted = converts_keys(json_content, case=case, inplace=True)
                response.content = self.json.dumps(converted)
            except ValueError:
                pass

        return response
