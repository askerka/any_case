from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from any_case import converts_keys
from .parser import case_format_parser
from .settings import AnyCaseSettings, django_settings
from .utils import is_json_content, is_json_possible, json, json_loads

__all__ = [
    'InputKeysConverterMixin',
    'KeysConverterMiddleware',
    'OutputKeysConverterMixin',
    'any_case_middleware_class',
]


class InputKeysConverterMixin:
    settings: AnyCaseSettings

    @classmethod
    def process_request(cls, request: HttpRequest) -> HttpRequest:
        if is_json_possible(request):
            try:
                json_body = json_loads(request)
                converted = converts_keys(
                    json_body, case='snake', inplace=True,
                    sep_numbers=cls.settings.SEP_NUMBERS_TO_SNAKE,
                )
                request.json = converted
            except ValueError:
                pass

        return request


class OutputKeysConverterMixin:
    settings: AnyCaseSettings

    @classmethod
    def process_response(
            cls,
            request: HttpRequest,
            response: HttpResponse,
    ) -> HttpResponse:
        if is_json_content(response):
            try:
                case = case_format_parser.parse(request, raise_exc=True)
                json_content = json.loads(response.content)
                converted = converts_keys(
                    json_content, case=case, inplace=True,
                    sep_numbers=cls.settings.sep_numbers(case),
                )
                response.content = json.dumps(converted)
            except ValueError:
                pass

        return response


def any_case_middleware_class(settings: AnyCaseSettings) -> MiddlewareMixin:
    bases = [MiddlewareMixin]

    if settings.CONVERT_INPUT_JSON:
        bases.append(InputKeysConverterMixin)
    if settings.has_convert_key:
        bases.append(OutputKeysConverterMixin)

    return type('KeysConverterMiddleware', tuple(bases), {'settings': settings})


KeysConverterMiddleware = any_case_middleware_class(django_settings)
