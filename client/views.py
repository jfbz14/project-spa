# Django
from django.views.generic import FormView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect

# Model
from .forms import FormProfileClient, FormUpdateProfileClient
from .models import ProfileClient, MedicalHistory


class CreateProfileClient(LoginRequiredMixin, FormView):
    """ Create client """

    template_name = 'profile_client/create_client.html'
    form_class = FormProfileClient
    success_url = reverse_lazy('profileclient:list_client')

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


class UpdateProfileClient(LoginRequiredMixin, UpdateView):
    """ Update model client """

    template_name: str = 'profile_client/update_client.html'
    pk_url_kwarg: str = 'id'
    form_class = FormUpdateProfileClient
    model = ProfileClient
    success_url = reverse_lazy('profileclient:list_client')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)


class ListViewClient(LoginRequiredMixin, ListView):
    """ Client all view. """

    template_name = 'profile_client/list_client.html'
    paginate_by = 15
    context_object_name = 'profileclient'  

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """validate search field, otherwise it returns the model"""

        data_search = self.request.GET.get('search')
        queryset = ProfileClient.objects.all()
        if data_search:
            queryset = queryset.filter(Q(document_number__icontains = data_search) | Q(first_name__icontains = data_search) | Q(last_name__icontains = data_search)).distinct()
        return queryset.order_by('first_name') 


class ListHistoryClient(LoginRequiredMixin, UpdateView):
    """ Update and view medicalhistoryclient """

    template_name = 'profile_client/update_view_history.html'
    pk_url_kwarg = 'id'
    model = MedicalHistory
    fields = [
        'allergies',
        'herpes',
        'Skin_illness',
        'condition',
        'cardiac',
        'hypertension',
        'diabetes',
        'thyroid',
        'autoimmune_disease',
        'surgical_history',
        'pregnancy','ication',
        'pacemaker','prosthesis',
        'diu',
        'implants',
        'others',
        ]
    success_url = reverse_lazy('profileclient:list_client')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)
