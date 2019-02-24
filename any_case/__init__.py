import re
from copy import deepcopy

from typing import List, TypeVar

__first_snake = re.compile(r'([^_])([A-Z][a-z]+)')
__second_snake = re.compile(r'([a-z])([A-Z])')
__sub_snake = r'\1_\2'


def to_snake_case(word: str) -> str:
    word = __first_snake.sub(__sub_snake, word)
    word = __second_snake.sub(__sub_snake, word)
    return word.lower()


__first_camel = re.compile(r'_([\w])([^_]+)')


def __sub_first_camel(match):
    return match.group(1).upper() + match.group(2).lower()


__second_camel = re.compile(r'([A-Z]+)([A-Z][a-z])')


def __sub_second_camel(match):
    return match.group(1).lower() + match.group(2)


def to_camel_case(word: str) -> str:
    word = __first_camel.sub(__sub_first_camel, word)
    word = __second_camel.sub(__sub_second_camel, word)
    return word[0].lower() + word[1:]


T = TypeVar('T')


def parse_keys(data: T, *, types='snake', inplace=False) -> T:
    if types not in {'camel', 'snake'}:
        raise ValueError('Invalid parse type, use `snake` or `camel`')

    if not inplace:
        data = deepcopy(data)

    formatter = to_camel_case if types == 'camel' else to_snake_case
    queue = [data]

    while queue:
        element = queue.pop()

        if isinstance(element, list):
            queue.extend(element)

        elif isinstance(element, dict):
            for key in list(element.keys())[:]:
                value = element[formatter(key)] = element.pop(key)

                if isinstance(value, list):
                    queue.extend(value)
                elif isinstance(value, dict):
                    queue.append(value)

    return data
