import json

import pytest
from django.test import RequestFactory


@pytest.fixture
def convert_input_json(settings):
    settings.ANY_CASE = {'CONVERT_INPUT_JSON': True}


pytestmark = pytest.mark.usefixtures('convert_input_json')


def test_convert_valid_post_json(middleware_factory):
    request = RequestFactory().post(
        '/', json.dumps({'camelCase': 'key'}), 'application/json',
    )

    middleware_factory().process_request(request)

    assert 'camel_case' in request.json


def test_just_text_with_json_content_type(middleware_factory):
    request = RequestFactory().post(
        '/', 'just_text', 'application/json',
    )
    middleware_factory().process_request(request)

    assert not hasattr(request, 'json')


def test_get_request_with_json_content_type(middleware_factory):
    request = RequestFactory().get(
        '/', {'camelCase': 'key'}, CONTENT_TYPE='application/json',
    )
    middleware_factory().process_request(request)

    assert not hasattr(request, 'json')


def test_sep_numbers(settings, middleware_factory):
    settings.ANY_CASE['SEP_NUMBERS_TO_SNAKE'] = True
    request = RequestFactory().post(
        '/', json.dumps({'camelCase12': 'key'}), 'application/json',
    )

    middleware_factory().process_request(request)

    assert request.json == {'camel_case_12': 'key'}
