# middleware.py
import logging

logger = logging.getLogger('django.request')

class LogAllRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(
            f"Request: {request.method} {request.get_full_path()} "
            f"User: {request.user if request.user.is_authenticated else 'Anonymous'}"
        )
        response = self.get_response(request)
        return response