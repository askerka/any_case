import json

import pytest
from django.conf import settings
from django.test import RequestFactory, override_settings

from any_case.contrib.django.parser import (
    django_case_format_parser, parse_body, parse_header, parse_query,
)
from any_case.contrib.django.settings import any_case_settings


def test_parse_header():
    request = RequestFactory().get('/', HTTP_ACCEPT_JSON_FORMAT='snake')

    assert 'snake' == parse_header('Accept-Json-Format', request)


def test_parse_query():
    request = RequestFactory().get('/?format=snake')

    assert 'snake' == parse_query('format', request)


def test_parse_body():
    request = RequestFactory().post(
        '/', json.dumps({'format': 'snake'}), 'application/json',
    )

    assert 'snake' == parse_body('format', request)


@pytest.fixture
def case_parser_factory():
    def factory():
        return django_case_format_parser(
            any_case_settings(settings)
        )

    return factory


@override_settings(ANY_CASE={
    'HEADER_KEY': 'Accept-Json-Format',
    'QUERY_KEY': 'format',
    'BODY_KEY': 'format'
})
def test__case_format_parser__found_key_in_body(case_parser_factory):
    request = RequestFactory().post(
        '/', json.dumps({'format': 'snake'}), 'application/json',
    )

    assert 'snake' == case_parser_factory().parse(request)


@override_settings(ANY_CASE={'HEADER_KEY': 'Accept-Json-Format'})
def test__case_format_parser__key_not_found(case_parser_factory):
    request = RequestFactory().post('/')

    assert case_parser_factory().parse(request) is None


@override_settings(ANY_CASE={'HEADER_KEY': 'Accept-Json-Format'})
def test__case_format_parser__key_found_but_unknown(case_parser_factory):
    request = RequestFactory().post('/', HTTP_ACCEPT_JSON_FORMAT='anaconda')

    with pytest.raises(ValueError):
        case_parser_factory().parse(request, raise_exc=True)
