import pytest
from django.test import RequestFactory


@pytest.fixture
def snake_request(settings):
    settings.ANY_CASE = {'HEADER_KEY': 'Accept-Json-Case'}
    return RequestFactory().get('/', HTTP_ACCEPT_JSON_CASE='snake')


def test_response_converted(middleware_factory, snake_request, json_response):
    middleware_factory().process_response(
        snake_request, json_response,
    )

    assert b'camel_case' in json_response.content


def test_request_without_case(middleware_factory, snake_request, json_response):
    snake_request.META.pop('HTTP_ACCEPT_JSON_CASE')

    middleware_factory().process_response(snake_request, json_response)

    assert b'camelCase' in json_response.content


def test_content_type_not_json(
        middleware_factory, snake_request, json_response,
):
    json_response['Content-Type'] = 'text/html; charset=utf-8'

    middleware_factory().process_response(snake_request, json_response)

    assert b'camelCase' in json_response.content


def test_content_not_json(middleware_factory, snake_request, json_response):
    json_response.content = 'just_text'

    middleware_factory().process_response(snake_request, json_response)

    assert b'just_text' in json_response.content


def test_request_has_no_content(
        middleware_factory, snake_request, json_response,
):
    json_response.content = ''

    middleware_factory().process_response(snake_request, json_response)

    assert not json_response.content
