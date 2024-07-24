from jwt.exceptions import ExpiredSignatureError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class SessionUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        return response


from django.middleware.csrf import CsrfViewMiddleware
from django.middleware.csrf import get_token
from django.http import HttpResponseForbidden

class CustomCsrfMiddleware(CsrfViewMiddleware):
    def process_request(self, request):
        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            self.process_csrf_token(request)
        return super().process_request(request)

    def process_csrf_token(self, request):
        csrf_token = get_token(request)
        if not self._validate_csrf_token(request, csrf_token):
            self._reject_csrf_token(request)

    def _validate_csrf_token(self, request, csrf_token):
        expected_token = request.headers.get('X-CSRFToken')
        return csrf_token == expected_token

    def _reject_csrf_token(self, request):
        return HttpResponseForbidden("CSRF Verification failed. Invalid token.")

    def _accept_csrf_token(self, request):
        pass

