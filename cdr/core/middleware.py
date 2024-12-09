from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

            # Interceptar errores HTTP específicos
            if response.status_code == 404:
                return self.handle_error(request, 404)
            elif response.status_code == 500:
                return self.handle_error(request, 500)

            return response

        # Manejo general de excepciones no controladas
        except Exception as e:
            return self.handle_exception(request, e)

    def handle_error(self, request, status_code):
        """Manejar errores HTTP específicos"""
        return render(request, 'core/error.html', {'status_code': status_code})

    def handle_exception(self, request, exception):
        """Manejar cualquier excepción no controlada"""
        if isinstance(exception, PermissionDenied):
            status_code = 403
        else:
            status_code = 500
        
        return render(request, 'core/error.html', {
            'status_code': status_code,
            'exception': str(exception),
        }, status=status_code)