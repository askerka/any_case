import copyreg
import re
# noinspection PyProtectedMember
from _collections_abc import dict_items, dict_keys, dict_values
from copy import deepcopy
from typing import Iterator, MappingView, TypeVar

__all__ = [
    'to_snake_case',
    'to_camel_case',
    'converts_keys',
    'camel_case_factory',
    'snake_case_factory',
]

__snake_first = re.compile(r'([^_])([A-Z][a-z]+)')
__snake_second = re.compile(r'([a-z])([A-Z])')
__snake_sub = r'\1_\2'

__numbers_first = re.compile(r'([a-zA-Z])(\d)')
__numbers_second = re.compile(r'(\d)([a-zA-Z])')
__numbers_sub = r'\1_\2'


def to_snake_case(word: str, sep_numbers: bool = False) -> str:
    word = __snake_first.sub(__snake_sub, word)
    word = __snake_second.sub(__snake_sub, word)
    if sep_numbers:
        word = __numbers_first.sub(__numbers_sub, word)
        word = __numbers_second.sub(__numbers_sub, word)
    return word.lower()


def snake_case_factory(sep_numbers: bool = False) -> callable:
    if sep_numbers:
        def formatter(word: str) -> str:
            word = __snake_first.sub(__snake_sub, word)
            word = __snake_second.sub(__snake_sub, word)
            word = __numbers_first.sub(__numbers_sub, word)
            word = __numbers_second.sub(__numbers_sub, word)
            return word.lower()
    else:
        def formatter(word: str) -> str:
            word = __snake_first.sub(__snake_sub, word)
            word = __snake_second.sub(__snake_sub, word)
            return word.lower()

    return formatter


__camel_first = re.compile(r'_([\w])([^_]*)')


def __camel_first_sub(match):
    return match.group(1).upper() + match.group(2).lower()


__camel_second = re.compile(r'([A-Z]+)([A-Z][a-z])')


def __camel_second_sub(match):
    return match.group(1).lower() + match.group(2)


def to_camel_case(word: str, sep_numbers: bool = False) -> str:
    word = __camel_first.sub(__camel_first_sub, word)
    word = __camel_second.sub(__camel_second_sub, word)
    if sep_numbers:
        word = __numbers_first.sub(__numbers_sub, word)
        word = __numbers_second.sub(__numbers_sub, word)
    return word[0].lower() + word[1:]


def camel_case_factory(sep_numbers: bool = False) -> callable:
    if sep_numbers:
        def formatter(word: str) -> str:
            word = __camel_first.sub(__camel_first_sub, word)
            word = __camel_second.sub(__camel_second_sub, word)
            word = __numbers_first.sub(__numbers_sub, word)
            word = __numbers_second.sub(__numbers_sub, word)
            return word[0].lower() + word[1:]
    else:
        def formatter(word: str) -> str:
            word = __camel_first.sub(__camel_first_sub, word)
            word = __camel_second.sub(__camel_second_sub, word)
            return word[0].lower() + word[1:]

    return formatter


def __pickle_dict_view(view):
    return lambda *x: list(x), view


copyreg.dispatch_table.update({
    dict_values: __pickle_dict_view,
    dict_keys: __pickle_dict_view,
    dict_items: __pickle_dict_view
})

T = TypeVar('T', dict, list)


def converts_keys(data: T, *, case: str = 'snake', inplace: bool = False, **kwargs) -> T:
    if case == 'camel':
        formatter = camel_case_factory(**kwargs)
    elif case == 'snake':
        formatter = snake_case_factory(**kwargs)
    else:
        raise ValueError('Invalid case format, use `snake` or `camel`')

    if not isinstance(data, (dict, list)):
        raise TypeError('Top container should be a dict or a list instance')

    if not inplace:
        data = deepcopy(data)

    queue = [data]

    while queue:
        element = queue.pop()

        if isinstance(element, list):
            queue.extend(element)

        elif isinstance(element, MappingView):
            # noinspection PyTypeChecker
            queue.extend(list(element))

        elif isinstance(element, dict):
            for key in tuple(element.keys()):
                new_key = formatter(key)
                value = element[new_key] = element.pop(key)

                if isinstance(value, list):
                    queue.extend(value)

                elif isinstance(value, dict):
                    queue.append(value)

                elif isinstance(value, (Iterator, MappingView)):
                    element[new_key] = value = list(value)
                    queue.extend(value)

    return data
