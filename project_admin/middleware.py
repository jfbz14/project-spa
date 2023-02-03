"""middleware login."""

# Django
from django.shortcuts import redirect
from django.urls import reverse


class ProfileLoginMiddleware:
    """
    Profile completion middleware.

    Make sure that all users who interact with the platform
    are registered.
    """

    def __init__(self, get_response):
        """Middleware initialization."""
        self.get_response = get_response

    def __call__(self, request):
        """Code to be executed for each request before the view is called."""
        if request.user.is_anonymous:
            if request.path not in [reverse('profileuser:login'), reverse('profileuser:logout')]:
                return redirect('profileuser:login')

        response = self.get_response(request)
        return response
