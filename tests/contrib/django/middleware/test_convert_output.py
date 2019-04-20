import json

import pytest
from django.http import HttpResponse
from django.test import RequestFactory

from any_case.contrib.django import KeysConverterMiddleware


@pytest.fixture
def snake_request(settings, reload_settings):
    settings.ANY_CASE = {'HEADER_KEY': 'Accept-Json-Case'}
    reload_settings()
    return RequestFactory().get('/', HTTP_ACCEPT_JSON_CASE='snake')


@pytest.fixture
def json_response():
    response = HttpResponse(status=200, content_type='application/json')
    response.content = json.dumps({'camelCase': 'value'})
    return response


def test_response_converted(snake_request, json_response):
    KeysConverterMiddleware(lambda: None).process_response(
        snake_request, json_response,
    )

    assert b'camel_case' in json_response.content


def test_request_without_case(snake_request, json_response):
    snake_request.META.pop('HTTP_ACCEPT_JSON_CASE')

    KeysConverterMiddleware(lambda: None).process_response(
        snake_request, json_response,
    )

    assert b'camelCase' in json_response.content


def test_content_type_not_json(snake_request, json_response):
    json_response['Content-Type'] = 'text/html; charset=utf-8'

    KeysConverterMiddleware(lambda: None).process_response(
        snake_request, json_response,
    )

    assert b'camelCase' in json_response.content


def test_content_not_json(snake_request, json_response):
    json_response.content = 'just_text'
    KeysConverterMiddleware(lambda: None).process_response(
        snake_request, json_response,
    )

    assert b'just_text' in json_response.content


def test_request_has_no_content(snake_request, json_response):
    json_response.content = ''
    KeysConverterMiddleware(lambda: None).process_response(
        snake_request, json_response,
    )

    assert not json_response.content
