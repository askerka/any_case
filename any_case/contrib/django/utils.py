from typing import Union

from django.http import HttpRequest, HttpResponse
from django.utils.functional import SimpleLazyObject

from .settings import django_settings

json = django_settings.JSON_MODULE


def json_loads(request: HttpRequest) -> Union[dict, list]:
    if hasattr(request, 'json'):
        return request.json

    return json.loads(request.body)


def is_json_possible(request: HttpRequest) -> bool:
    return bool(
            request.method not in {'GET', 'HEAD'} and
            request.content_type == 'application/json' and
            request.body
    )


def is_json_content(response: HttpResponse) -> bool:
    return bool(
            response.get('Content-Type') == 'application/json' and
            response.content
    )
