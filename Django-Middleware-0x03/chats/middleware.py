import logging
from datetime import datetime
from django.http import HttpResponseForbidden

logger = logging.getLogger("request_logger")

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
         # Get current server hour (24-hour format)
        current_hour = datetime.now().hour

        # Allow only between 6 AM (06:00) and 9 PM (21:00)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access to the chat is restricted at this time.")

        response = self.get_response(request)
        return response