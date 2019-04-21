import pytest

from any_case import to_snake_case, to_camel_case, converts_keys


@pytest.mark.parametrize(['source', 'expected'], [
    ('camelCase', 'camel_case'),
    ('PascalCase', 'pascal_case'),
    ('HTTPResponse', 'http_response'),
    ('longCamelCase', 'long_camel_case'),

    ('snake_case', 'snake_case'),
    ('Camel_Case', 'camel_case'),
    ('CONST_CASE', 'const_case'),
])
def test_convert_to_snake(source, expected):
    assert to_snake_case(source) == expected


@pytest.mark.parametrize(['source', 'expected'], [
    ('snake_case', 'snakeCase'),
    ('Mixed_Case', 'mixedCase'),
    ('CONST_CASE', 'constCase'),
    ('long_snake_case', 'longSnakeCase'),

    ('camelCase', 'camelCase'),
    ('PascalCase', 'pascalCase'),
    ('HTTPResponse', 'httpResponse'),
])
def test_convert_to_camel(source, expected):
    assert to_camel_case(source) == expected


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
    converted = converts_keys(data, case='snake')
    deep_value = converted['key']['sub_key'][0]['sub_sub_key']['deep_key']
    assert deep_value == 'camelValue'
