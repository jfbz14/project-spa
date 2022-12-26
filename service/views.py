# Django
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum 
from django.db.models.functions import Coalesce

#model
from service.models import Service, ItemService
from .forms import FormCreateItemservice


#view service

class CreateService(LoginRequiredMixin, CreateView):
    """ create service """

    template_name = 'service/create_service.html'
    model = Service 
    fields = ['name', 'time_minutes', 'commission_percentage', 'price']
    success_url = reverse_lazy('service:list_service')  

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)


class UpdateService(LoginRequiredMixin, UpdateView):
    """ update service """

    template_name = 'service/update_service.html'
    pk_url_kwarg = 'id'
    model = Service
    fields = ['name', 'time_minutes', 'commission_percentage', 'price']
    success_url = reverse_lazy('service:list_service')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)
        

class ListViewService(LoginRequiredMixin, ListView):
    """ service all view. """

    template_name = 'service/list_service.html'
    model = Service
    paginate_by = 15
    context_object_name = 'service'

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """receives the field to search"""
        data_search = self.request.GET.get('search')
        queryset =Service.objects.all()
        if data_search:
            queryset = queryset.filter(name__icontains = data_search)
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        # Update items
        item_reload = ItemService.objects.all()
        for i in item_reload:
            i.save()
        context = super().get_context_data(**kwargs)
        cost_service = Service.objects.filter().annotate(id_service=Coalesce('pk', 'pk')).annotate(sum_cost=Sum('itemservice__price_amount')).values('id_service', 'sum_cost')       
        context["cost_service"] = cost_service
        return context
        

#Itemservice
class CreateItemService(LoginRequiredMixin, CreateView):
    """ create itemservice """

    template_name = 'service/itemservice/create_itemservice.html'
    model = ItemService
    form_class = FormCreateItemservice

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """ check if the article in use """

        query_valid = ItemService.objects.filter(service=self.kwargs.get("id"), article=form.data['article']).exists()
        if query_valid:
            self.extra_context = {'item_in_use': 'Article is alredy in use'}
            return super().form_invalid(form)
        self.object = form.save()    
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add room to context."""
        context = super().get_context_data(**kwargs)
        service = Service.objects.get(id=self.kwargs.get("id"))
        context['service'] = service
        return context

    def get_success_url(self):
        """Return to list itemroom."""
        id = self.kwargs.get("id")
        return reverse('service:list_itemservice', kwargs={'id': id})


class ListViewItemService(LoginRequiredMixin, ListView):
    """ itemservice all view. """

    template_name = 'service/itemservice/list_itemservice.html'
    pk_url_kwarg = 'id'
    paginate_by = 15
    context_object_name = 'itemservice'

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        id = self.kwargs.get("id")
        data_search = self.request.GET.get('search')
        data_update_amount = self.request.GET.get('update_amount')
        data_update_amount_id = self.request.GET.get('update_amount_id')

        if data_update_amount:
            try:
                data_update_amount = int(data_update_amount)
            except:
                data_update_amount = None  

        #Update item 
        if data_update_amount and data_update_amount_id:
            item_service = get_object_or_404(ItemService, id=data_update_amount_id)
            item_service.amount = data_update_amount
            item_service.save() 

        queryset = ItemService.objects.filter(service__id=id)
        if data_search:
            queryset = queryset.filter(article__article__icontains = data_search)
        return queryset  

    def get_context_data(self, **kwargs):
        """Add id service to context."""
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        service = get_object_or_404(Service, id=id)
        context['service'] = service
        return context   


class DeleteItemService(LoginRequiredMixin, DeleteView):
    """itemservice delete"""

    template_name = 'service/itemservice/delete_itemservice.html'
    pk_url_kwarg = 'id'
    model = ItemService

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Return to list itemservice."""
        id = self.object.service.id
        return reverse('service:list_itemservice', kwargs={'id': id})