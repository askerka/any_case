from functools import partial
from typing import KeysView

import pytest

from any_case import converts_keys, to_camel_case, to_snake_case
from any_case.converter import camel_case_factory, snake_case_factory


@pytest.mark.parametrize(['source', 'expected'], [
    ('camelCase', 'camel_case'),
    ('PascalCase', 'pascal_case'),
    ('HTTPResponse', 'http_response'),
    ('longCamelCase', 'long_camel_case'),

    ('snake_case', 'snake_case'),
    ('Camel_Case', 'camel_case'),
    ('CONST_CASE', 'const_case'),

    ('123CamelCase', '123_camel_case'),
    ('123camelCase', '123camel_case'),
    ('camel123Case', 'camel123_case'),
    ('camel123case', 'camel123case'),
    ('camelCase123', 'camel_case123'),
])
@pytest.mark.parametrize('formatter', [to_snake_case, snake_case_factory()])
def test_convert_to_snake(source, expected, formatter):
    assert to_snake_case(source) == expected


@pytest.mark.parametrize(['source', 'expected'], [
    ('123CamelCase', '123_camel_case'),
    ('123camelCase', '123camel_case'),
    ('camel123Case', 'camel_123_case'),
    ('camel123case', 'camel_123case'),
    ('camelCase123', 'camel_case_123'),
])
@pytest.mark.parametrize('formatter', [
    partial(to_snake_case, sep_numbers=True),
    snake_case_factory(sep_numbers=True)
])
def test_convert_to_snake_with_numbers(source, expected, formatter):
    assert formatter(source) == expected


@pytest.mark.parametrize(['source', 'expected'], [
    ('snake_case', 'snakeCase'),
    ('Mixed_Case', 'mixedCase'),
    ('CONST_CASE', 'constCase'),
    ('long_snake_case', 'longSnakeCase'),

    ('camelCase', 'camelCase'),
    ('PascalCase', 'pascalCase'),
    ('HTTPResponse', 'httpResponse'),

    ('123_camel_case', '123CamelCase'),
    ('123camel_case', '123camelCase'),
    ('camel_case123', 'camelCase123'),
    ('camel_case_123', 'camelCase123'),
    ('camel_123_case', 'camel123Case'),
    ('camel_123case', 'camel123case'),
    ('camel_case_1', 'camelCase1'),
    ('camel_1_case', 'camel1Case'),
    ('camel_1case', 'camel1case'),
    ('1_camel_case', '1CamelCase'),
    ('1camel_case', '1camelCase'),
])
@pytest.mark.parametrize('formatter', [to_camel_case, camel_case_factory()])
def test_convert_to_camel(source, expected, formatter):
    assert formatter(source) == expected


@pytest.mark.parametrize(['source', 'expected'], [
    ('123_camel_case', '123_CamelCase'),
    ('123camel_case', '123camelCase'),
    ('camel_123_case', 'camel_123_Case'),
    ('camel_123case', 'camel_123case'),
    ('camel_case123', 'camelCase123'),
    ('camel_case_123', 'camelCase_123'),
])
@pytest.mark.parametrize('formatter', [
    partial(to_camel_case, sep_numbers=True),
    camel_case_factory(sep_numbers=True)
])
def test_convert_to_camel_with_numbers(source, expected, formatter):
    assert formatter(source) == expected


def test_convert_with_numbers():
    assert to_snake_case(
        to_camel_case(
            'camel_case_123', sep_numbers=True
        ), sep_numbers=True,
    ) == 'camel_case_123'

    assert to_camel_case(
        to_snake_case(
            'camelCase123', sep_numbers=False
        ), sep_numbers=False,
    ) == 'camelCase123'


@pytest.mark.parametrize('values', [
    [1, 2, 3], 1, 1.0, 'string', (1, 2, 3), {1, 2, 3}, [1, [2], 3]
])
def test_simple_types_not_converted(values):
    assert converts_keys({'key': values}) == {'key': values}


def test_convert_nested_data():
    data = {
        'key': {
            'subKey': [
                {
                    'subSubKey': {
                        'deepKey': 'camelValue'
                    }

                }
            ]
        }
    }
    converted = converts_keys(data, case='snake', inplace=True)
    deep_value = converted['key']['sub_key'][0]['sub_sub_key']['deep_key']

    assert deep_value == 'camelValue'


def test_convert_dict_values():
    data = {
        'key': {
            '1': {'snake_case': 'value'},
            '2': {'snake_case': 'value'},
            '3': {'snake_case': 'value'},
        }.values(),
        'simple': {'1': 1, '2': 2, '3': 3}.keys()
    }
    result = converts_keys(data, case='camel')

    assert result['key'] == [{'snakeCase': 'value'}] * 3
    assert result['simple'] == list(data['simple'])
    assert isinstance(data['simple'], KeysView)


def test_convert_dict_values_inplace():
    data = {'key': {'inner': {'snake_case': 'value'}}.values()}
    converts_keys(data, case='camel', inplace=True)

    assert data['key'] == [{'snakeCase': 'value'}]


def test_convert_wrong_data_container():
    data = {'snake_case': 'value'}.values()

    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        converts_keys(data, case='snake')


def test_convert_keys_with_numbers():
    data = {'snake_case_1': 'value'}
    converts_keys(data, case='camel', inplace=True, sep_numbers=True)
    assert data == {'snakeCase_1': 'value'}
