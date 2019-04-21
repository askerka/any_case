import json

import pytest
from django.http import HttpResponse

from any_case.contrib.django.middleware import any_case_middleware_class
from any_case.contrib.django.settings import any_case_settings


@pytest.fixture
def middleware_factory():
    def factory():
        from django.conf import settings

        cls = any_case_middleware_class(
            any_case_settings(settings)
        )
        return cls(lambda: None)

    return factory


@pytest.fixture
def json_response():
    response = HttpResponse(status=200, content_type='application/json')
    response.content = json.dumps({'camelCase': 'value'})
    return response
