import re
from copy import deepcopy

from typing import TypeVar

__snake_first = re.compile(r'([^_])([A-Z][a-z]+)')
__snake_second = re.compile(r'([a-z])([A-Z])')
__snake_sub = r'\1_\2'


def to_snake_case(word: str) -> str:
    word = __snake_first.sub(__snake_sub, word)
    word = __snake_second.sub(__snake_sub, word)
    return word.lower()


__camel_first = re.compile(r'_([\w])([^_]+)')


def __camel_first_sub(match):
    return match.group(1).upper() + match.group(2).lower()


__camel_second = re.compile(r'([A-Z]+)([A-Z][a-z])')


def __camel_second_sub(match):
    return match.group(1).lower() + match.group(2)


def to_camel_case(word: str) -> str:
    word = __camel_first.sub(__camel_first_sub, word)
    word = __camel_second.sub(__camel_second_sub, word)
    return word[0].lower() + word[1:]


T = TypeVar('T')


def converts_keys(data: T, *, case='snake', inplace=False) -> T:
    if case == 'camel':
        formatter = to_camel_case
    elif case == 'snake':
        formatter = to_snake_case
    else:
        raise ValueError('Invalid case type, use `snake` or `camel`')

    if not inplace:
        data = deepcopy(data)

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
