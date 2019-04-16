from typing import Any, Union

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .django.parser import case_format_parser
from ..converter import converts_keys


class AnyCaseJSONParser(JSONParser):
    def parse(
            self,
            stream,
            media_type: str = None,
            parser_context: dict = None,
    ) -> Any:
        data = super().parse(stream, media_type, parser_context)
        data = converts_keys(data, case='snake', inplace=True)
        return data


class AnyCaseJSONRenderer(JSONRenderer):
    def render(
            self,
            data: Union[dict, list],
            accepted_media_type: str = None,
            renderer_context: dict = None
    ) -> bytes:
        renderer_context = renderer_context or {}
        request = renderer_context['request']

        case = case_format_parser.parse(request)
        if case:
            data = converts_keys(data, case=case, inplace=True)

        return super().render(data, accepted_media_type, renderer_context)
