import json

import pytest
from django.test import RequestFactory

from any_case.contrib.django import KeysConverterMiddleware


@pytest.fixture
def any_case_settings(settings, reload_settings):
    settings.ANY_CASE = {'CONVERT_INPUT_JSON': True}
    reload_settings()


pytestmark = pytest.mark.usefixtures('any_case_settings')


def test_convert_valid_post_json():
    request = RequestFactory().post(
        '/', json.dumps({'camelCase': 'key'}), 'application/json',
    )

    KeysConverterMiddleware(lambda: None).process_request(request)

    assert 'camel_case' in request.json


def test_just_text_with_json_content_type():
    request = RequestFactory().post(
        '/', 'just_text', 'application/json',
    )
    KeysConverterMiddleware(lambda: None).process_request(request)

    assert not hasattr(request, 'json')


def test__get_request_with_json_content_type():
    request = RequestFactory().get(
        '/', {'camelCase': 'key'}, CONTENT_TYPE='application/json',
    )
    KeysConverterMiddleware(lambda: None).process_request(request)

    assert not hasattr(request, 'json')
