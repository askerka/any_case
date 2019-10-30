from any_case.contrib.django.settings import AnyCaseSettings


def test_sep_numbers():
    settings = AnyCaseSettings({
        'SEP_NUMBERS_TO_SNAKE': False,
        'SEP_NUMBERS_TO_CAMEL': True,
    })

    assert not settings.sep_numbers('snake')
    assert settings.sep_numbers('camel')


def test_has_convert_key():
    settings = AnyCaseSettings({
        'HEADER_KEY': None,
        'QUERY_KEY': None,
        'BODY_KEY': None,
    })

    assert not settings.has_convert_key
