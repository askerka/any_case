from typing import List, Callable, Any, Optional

Parser = Callable[[Any], Optional[str]]


class CaseFormatParser:
    def __init__(self, parsers: List[Parser]) -> None:
        self.parsers = parsers

    def parse(self, request: Any, raise_exc: bool = False) -> Optional[str]:
        case = None

        for parser in self.parsers:
            case = parser(request)
            if case:
                case = case.lower()
                break

        # TODO Replace set to Enum if the number of cases will be more than two
        if case is None or case not in {'snake', 'camel'}:
            if raise_exc:
                raise ValueError('Did not found known case format')
            else:
                case = None

        return case
