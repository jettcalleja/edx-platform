"""Tests for header_control middleware."""
from django.http import HttpResponse, HttpRequest
from django.test import TestCase
from header_control import remove_headers_from_response, force_header_for_response
from header_control.middleware import HeaderControlMiddleware


class TestHeaderControlMiddlewareProcessResponse(TestCase):
    """Test the `header_control` middleware. """
    def setUp(self):
        super(TestHeaderControlMiddlewareProcessResponse, self).setUp()
        self.middleware = HeaderControlMiddleware()

    def test_removes_intended_headers(self):
        fake_request = HttpRequest()

        fake_response = HttpResponse()
        fake_response['Vary'] = 'Cookie'
        fake_response['Accept-Encoding'] = 'gzip'
        remove_headers_from_response(fake_response, 'Vary')

        result = self.middleware.process_response(fake_request, fake_response)
        self.assertNotIn('Vary', result)
        self.assertEquals('gzip', result['Accept-Encoding'])

    def test_forces_intended_header(self):
        fake_request = HttpRequest()

        fake_response = HttpResponse()
        fake_response['Vary'] = 'Cookie'
        fake_response['Accept-Encoding'] = 'gzip'
        force_header_for_response(fake_response, 'Vary', 'Origin')

        result = self.middleware.process_response(fake_request, fake_response)
        self.assertEquals('Origin', result['Vary'])
        self.assertEquals('gzip', result['Accept-Encoding'])

    def test_does_not_mangle_undecorated_response(self):
        fake_request = HttpRequest()

        fake_response = HttpResponse()
        fake_response['Vary'] = 'Cookie'
        fake_response['Accept-Encoding'] = 'gzip'

        result = self.middleware.process_response(fake_request, fake_response)
        self.assertEquals('Cookie', result['Vary'])
        self.assertEquals('gzip', result['Accept-Encoding'])
