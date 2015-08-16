from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from astroid import MANAGER
from astroid.builder import AstroidBuilder

BASE_REQUEST_DEFINITION = """
from django.http import HttpResponse, HttpRequest

def request(self, *args, **kwargs):
    resp = HttpResponse()
    resp.client = self
    resp.content = ''
    resp.context = {}
    resp.request = HttpRequest()
    resp.templates = []
    %s
    return resp
"""
DJANGO_REQUEST_DEFINITION = BASE_REQUEST_DEFINITION % ''
DRF_REQUEST_DEFINITION = BASE_REQUEST_DEFINITION % 'resp.data = {}'
DJANGO_CLIENT_REQUEST = AstroidBuilder(
    MANAGER).string_build(DJANGO_REQUEST_DEFINITION).locals['request']
DRF_CLIENT_REQUEST = AstroidBuilder(
    MANAGER).string_build(DRF_REQUEST_DEFINITION).locals['request']


def transform_test_response(cls):
    if cls.is_subtype_of('django.test.client.Client'):
        cls.locals['request'] = DJANGO_CLIENT_REQUEST
    elif cls.is_subtype_of('rest_framework.test.APIClient'):
        cls.locals['request'] = DRF_CLIENT_REQUEST
