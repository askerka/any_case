import json

from django.test import RequestFactory

from any_case.contrib.django import KeysConverterMiddleware


def test__valid_post_json():
    request = RequestFactory().post(
        '/', json.dumps({'camelCase': 'key'}), 'application/json',
    )

    KeysConverterMiddleware(lambda: None).process_request(request)

    body = json.loads(request.body)
    assert body['camel_case']


def test__just_text_with_json_content_type():
    pass


def test__get_request_with_json_content_type():
    pass
