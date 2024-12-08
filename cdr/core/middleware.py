from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Interceptar errores 404
        if isinstance(response, HttpResponseNotFound):
            return self.handle_error(request, 404)

        # Interceptar errores 500
        if isinstance(response, HttpResponseServerError):
            return self.handle_error(request, 500)

        return response

    def handle_error(self, request, status_code):
        return render(request, 'core/error.html', {'status_code': status_code})