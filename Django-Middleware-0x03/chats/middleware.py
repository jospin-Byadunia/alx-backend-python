import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict

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
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.offensive_words = {"badword1", "badword2", "badword3"}  # Add more offensive words as needed

    def __call__(self, request):
        # Only track POST requests (chat messages)
        if request.method == "POST":
            client_ip = self.get_client_ip(request)
            now = time.time()

            # Keep only requests made in the last 60 seconds
            self.ip_requests[client_ip] = [
                ts for ts in self.ip_requests[client_ip] if now - ts < 60
            ]

            # If already 5 requests in the last minute → block
            if len(self.ip_requests[client_ip]) >= 5:
                return HttpResponseForbidden(
                    "You have exceeded the message limit (5 per minute). Please wait."
                )

            # Otherwise record this request
            self.ip_requests[client_ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Retrieve client IP (supports X-Forwarded-For for proxies)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)

        # Only allow authenticated users with role 'admin' or 'moderator'
        if not user or not user.is_authenticated:
            return HttpResponseForbidden("Access denied. You must be logged in.")

        if getattr(user, 'role', '').lower() not in ['admin', 'moderator']:
            return HttpResponseForbidden("Access denied. Insufficient permissions.")

        response = self.get_response(request)
        return response