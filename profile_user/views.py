# Django
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Model
from profile_user.forms import SignupFormUser, UpdateFormUser
from profile_user.models import ProfileUser, User


class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'profile_user/login.html'

    def dispatch(self, request,*args, **kwargs):
        """ user started, redirect to start """

        if request.user.is_authenticated:
            return redirect('booking:list_booking_wait_gestion')
            
        return super().dispatch(request, *args, **kwargs)


class SignupView(LoginRequiredMixin, FormView):
    """User signup view."""

    template_name = 'profile_user/signup.html'
    form_class = SignupFormUser
    success_url = reverse_lazy('profileuser:list_profile')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


class ListViewProfile(LoginRequiredMixin, ListView):
    """ profile all view. """

    template_name = 'profile_user/list_profile.html'
    paginate_by = 12
    context_object_name = 'profile'  

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs) 
    
    def get_queryset(self):
        """validate search field, otherwise it returns the model"""

        data_search = self.request.GET.get('search')
        queryset = ProfileUser.objects.all()
        if data_search:
            queryset = queryset.filter(Q(user__first_name__icontains = data_search) | Q(user__last_name__icontains = data_search)).distinct()
        return queryset.order_by('user__first_name').exclude(Q(user__is_staff=True) | Q(user__is_active=False))


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """profile update"""

    template_name = 'profile_user/update_profile.html'
    pk_url_kwarg = 'id'
    form_class = UpdateFormUser
    model = ProfileUser
    success_url = reverse_lazy('profileuser:list_profile')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        firts_name = self.request.POST['first_name']
        lasts_name = self.request.POST['last_name']
        email = self.request.POST['email']

        try:
            """Check if it is email."""
            validate_email(email)
        except ValidationError:
            self.extra_context = {'email_errors': 'Email ({}) is invalid.'.format(email)}
            return super().form_invalid(form) 
                
        if firts_name and lasts_name and email:
            id = self.object.user.id
            user = get_object_or_404(User, id=id)

            valid_email = User.objects.filter(email=email).exclude(id=user.pk).exists()
            if valid_email:
                """Email must be unique."""
                self.extra_context = {'email_errors': 'Email ({}) is already in use.'.format(email)}
                return super().form_invalid(form) 

            user.first_name = firts_name
            user.last_name = lasts_name
            user.email = email
            user.save()
            form.save()
            return super().form_valid(form)
        return super().form_invalid(form)    
            

class UserPasswordChangeView (LoginRequiredMixin, PasswordChangeView):
    """ Change password"""

    template_name = 'profile_user/password_change.html'
    success_url = reverse_lazy('profileuser:list_profile')


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'profile_user/logged_out.html'        
