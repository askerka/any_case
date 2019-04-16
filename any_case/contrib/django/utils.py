from abc import ABC, abstractmethod
from typing import Any, Union

from django.http import HttpRequest

from .settings import django_setting

json = django_setting.JSON_MODULE


class Encoder(ABC):
    @abstractmethod
    def loads(self, *args, **kwargs) -> Any:
        pass


def json_loads(request: HttpRequest) -> Union[dict, list]:
    body = request.body
    if isinstance(request.body, str):
        body = json.loads(request.body)
    return body
