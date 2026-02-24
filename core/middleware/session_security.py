import time
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth
from django.conf import settings

class DashboardSecurityMiddleware:
    """
    Middleware to enforce strict session timeout for dashboard URLs.
    If a user is inactive in the dashboard for more than a set time (e.g., 2 minutes),
    they are automatically logged out.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We only care about authenticated users accessing the dashboard
        if request.user.is_authenticated and request.path.startswith('/dashboard/'):
            last_activity = request.session.get('dashboard_last_activity')
            current_time = int(time.time())

            # SESSION_TIMEOUT_DASHBOARD in seconds (e.g., 60 for 1 minute)
            timeout = getattr(settings, 'SESSION_TIMEOUT_DASHBOARD', 60)

            if last_activity:
                elapsed = current_time - last_activity
                if elapsed > timeout:
                    # Session expired due to inactivity
                    auth.logout(request)
                    return redirect(settings.LOGIN_URL + '?next=' + request.path)

            # Update last activity timestamp
            request.session['dashboard_last_activity'] = current_time

        return self.get_response(request)
