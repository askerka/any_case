import json

import pytest
from django.test import RequestFactory

import any_case.contrib.django.parser as any_case_parser


@pytest.mark.parametrize('header_key', ['Accept-Json-Case', None])
@pytest.mark.parametrize('query_key', ['case', None])
@pytest.mark.parametrize('body_key', ['case', None])
def test_parser_properly_configured_from_settings(
        settings, header_key, query_key, body_key, reload_settings
):
    settings.ANY_CASE = {
        'HEADER_KEY': header_key,
        'QUERY_KEY': query_key,
        'BODY_KEY': body_key
    }
    reload_settings()

    case_parser = any_case_parser.case_format_parser
    enabled_parsers = len(list(filter(None, [header_key, query_key, body_key])))
    distinct_parsers = len(set(map(id, case_parser.parsers)))

    assert len(case_parser.parsers) == enabled_parsers
    assert distinct_parsers == enabled_parsers


def test_parse_header(settings, reload_settings):
    settings.ANY_CASE = {'HEADER_KEY': 'Accept-Json-Case'}
    reload_settings()
    request = RequestFactory().get('/', HTTP_ACCEPT_JSON_CASE='snake')

    assert 'snake' == any_case_parser.parse_header(request)


def test_parse_query(settings, reload_settings):
    settings.ANY_CASE = {'QUERY_KEY': 'case'}
    reload_settings()
    request = RequestFactory().get('/?case=snake')

    assert 'snake' == any_case_parser.parse_query(request)


def test_parse_body(settings, reload_settings):
    settings.ANY_CASE = {'BODY_KEY': 'case'}
    reload_settings()
    request = RequestFactory().post(
        '/', json.dumps({'case': 'snake'}), 'application/json',
    )

    assert 'snake' == any_case_parser.parse_body(request)


def test__parser__found_key_in_body(settings, reload_settings):
    settings.ANY_CASE = {
        'HEADER_KEY': 'Accept-Json-Case',
        'QUERY_KEY': 'case',
        'BODY_KEY': 'case'
    }
    reload_settings()

    request = RequestFactory().post(
        '/', json.dumps({'case': 'snake'}), 'application/json',
    )
    case_parser = any_case_parser.case_format_parser

    assert 'snake' == case_parser.parse(request)


def test__case_format_parser__key_not_found(settings, reload_settings):
    settings.ANY_CASE = {'HEADER_KEY': 'Accept-Json-Case'}
    reload_settings()

    request = RequestFactory().post('/')
    case_parser = any_case_parser.case_format_parser

    assert case_parser.parse(request) is None


def test__case_format_parser__key_found_but_unknown(settings, reload_settings):
    settings.ANY_CASE = {'HEADER_KEY': 'Accept-Json-Case'}
    reload_settings()

    request = RequestFactory().post('/', HTTP_ACCEPT_JSON_CASE='anaconda')
    case_parser = any_case_parser.case_format_parser

    with pytest.raises(ValueError):
        case_parser.parse(request, raise_exc=True)
