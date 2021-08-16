from django.http import HttpResponse
from rest_framework_api_key.permissions import KeyParser
from django.conf import settings


class KeyOnlyInHeaderParser(KeyParser):
    def get_from_authorization(self, request):
        return None


class ApiKeyHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._key_parser = KeyOnlyInHeaderParser()

    def __call__(self, request):
        key = self._key_parser.get(request)
        if not key or key != settings.API_KEY:
            return HttpResponse('Unauthorized', status=401)
        return self.get_response(request)
