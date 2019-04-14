from typing import List, Callable, Any, Optional

from django.http import HttpRequest


Parser = Callable[[Any], Optional[str]]


class CaseFormatParser:
    def __init__(self, parsers: List[Parser]) -> None:
        self.parsers = parsers

    def parse(self, request: HttpRequest) -> str:
        case = None

        for parser in self.parsers:
            case = parser(request)
            if case:
                case = case.lower()
                break

        # TODO Replace case variants to Enum
        if case is None or case not in {'snake', 'camel'}:
            raise ValueError('Did not found known case format')

        return case
