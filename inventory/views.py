from django.views.generic import UpdateView, ListView, CreateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q, Sum 
from django.db.models.functions import Coalesce

#model
import datetime
from inventory.forms import FormCreateSupplie, FormDistributor, FormClassification, FormUpdateSupplie, FormCreateItemRoom
from inventory.models import *

#distributor

class CreateDistributor(LoginRequiredMixin, CreateView):
    """ Created distributor. """

    template_name = 'inventory/distributor/create_distributor.html'
    model = Distributor
    form_class = FormDistributor
    success_url = reverse_lazy('inventory:list_distributor')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

  
class UpdateDistributor(LoginRequiredMixin, UpdateView):
    """ Update distributor. """

    template_name = 'inventory/distributor/update_distributor.html'
    pk_url_kwarg = 'id'
    model = Distributor
    form_class = FormDistributor
    success_url = reverse_lazy('inventory:list_distributor')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)


class ListViewDistributor(LoginRequiredMixin, ListView):
    """ distributor all view. """

    template_name = 'inventory/distributor/list_distributor.html'
    model = Distributor
    paginate_by = 15
    context_object_name = 'distributors'  

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """validate search field, otherwise it returns the model"""

        data_search = self.request.GET.get('search')
        queryset = Distributor.objects.all()
        if data_search:
            queryset = queryset.filter(Q(name_distributor__icontains = data_search) | Q(name_contact__icontains = data_search)).distinct()
        return queryset  


# ClassificatioSupplie
class CreateClassificationSupplie(LoginRequiredMixin, CreateView):
    """ create classificatioSupplie """

    template_name = 'inventory/classificationsupplie/create_classificationsupplie.html'
    model = ClassificatioSupplie
    form_class = FormClassification
    success_url = reverse_lazy('inventory:list_classificationsupplie')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

   
class ListViewClassificationSupplie(LoginRequiredMixin, ListView):
    """ Classificatiosupplie all view. """

    template_name = 'inventory/classificationsupplie/list_classificationsupplie.html'
    model = ClassificatioSupplie
    paginate_by = 5
    context_object_name = 'classificationsupplie'   

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """validate search field, otherwise it returns the model"""

        data_search = self.request.GET.get('search')
        data_update_classificationsupplie = self.request.GET.get('update_classificationsupplie')
        data_update_classificationsupplie_id = self.request.GET.get('update_classificationsupplie_id')

        #Update name area classification
        if data_update_classificationsupplie and data_update_classificationsupplie_id:
            update_classificationsupplie = get_object_or_404(ClassificatioSupplie, id=data_update_classificationsupplie_id)
            update_classificationsupplie.name_area = data_update_classificationsupplie
            update_classificationsupplie.save() 

        queryset = ClassificatioSupplie.objects.all()
        if data_search:
            queryset = queryset.filter(name_area__icontains = data_search)
        return queryset.order_by('name_area')  
    

# Supplie
class CreateSupplie(LoginRequiredMixin, FormView):
    """ create supplie """

    template_name = 'inventory/supplie/create_supplie.html'
    form_class = FormCreateSupplie
    success_url = reverse_lazy('inventory:list_supplie')

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

  
class UpdateSupplie(LoginRequiredMixin, UpdateView):
    """supplie update"""

    template_name = 'inventory/supplie/update_supplie.html'
    pk_url_kwarg = 'id'
    model = Supplie
    form_class = FormUpdateSupplie
    success_url = reverse_lazy('inventory:list_supplie') 

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)


class ListViewSupplie(LoginRequiredMixin, ListView):
    """ Supplie all view. """

    template_name = 'inventory/supplie/list_supplie.html'
    paginate_by = 15
    context_object_name = 'supplie'  

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """ Validate search field, otherwise it returns the model. """

        data_search = self.request.GET.get('search')
        queryset = Supplie.objects.all()
        if data_search:
            queryset = queryset.filter(article__icontains = data_search)
        return queryset.order_by('article')   


# Cellarglobal 
class ListViewCellarGlobal(LoginRequiredMixin, ListView):
    """ Cellarglobal all view. """

    template_name = 'inventory/cellarglobal/list_cellarglobal.html'
    paginate_by = 15
    context_object_name = 'cellarglobal'  

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        # Update model
        queryset = CellarGlobal.objects.all()
        for i in queryset:
            i.save()

        data_search = self.request.GET.get('search')
        data_update_in_cellar_balance = self.request.GET.get('update_in_cellar_balance')
        data_update_in_cellar_balance_id = self.request.GET.get('update_in_cellar_balance_id')

        if data_update_in_cellar_balance:
            try:
                data_update_in_cellar_balance = int(data_update_in_cellar_balance)
            except:
                data_update_in_cellar_balance = None  
        
        #Update field balance
        if data_update_in_cellar_balance and data_update_in_cellar_balance_id:
            cellar = get_object_or_404(CellarGlobal, id=data_update_in_cellar_balance_id)
            cellar.in_cellar_balance = data_update_in_cellar_balance
            cellar.save()

        if data_search:
           queryset = queryset.filter(article__article__icontains = data_search)

        return queryset.order_by('article__article') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data_search = self.request.GET.get('search') 
        data_start = self.request.GET.get('start')
        data_end = self.request.GET.get('end')
        
        try:
            if data_start:
                data_start=datetime.datetime.strptime(data_start,'%Y-%m-%d').date()
                if data_end:
                    data_end=datetime.datetime.strptime(data_end,'%Y-%m-%d').date()
        except:
            data_start = None 
            data_end = None

        incellar = InCellar.objects.all()
        outcellar = OutCellar.objects.all()
        if data_search and data_start and data_end:
            incellar = incellar.filter(article__article__icontains = data_search).filter(date__date__range=[data_start, data_end])
            outcellar = outcellar.filter(article__article__icontains = data_search).filter(date__date__range=[data_start, data_end])
        elif data_start and data_end:
            incellar = incellar.filter(date__date__range=[data_start, data_end])
            outcellar = outcellar.filter(date__date__range=[data_start, data_end])

        incellar = incellar.filter().annotate(supplie=Coalesce('article', 'article')).values('supplie').annotate(cant=Sum('amount'))
        outcellar = outcellar.filter().annotate(supplie=Coalesce('article', 'article')).values('supplie').annotate(cant=Sum('amount'))
        context["incellar"] = incellar
        context["outcellar"] = outcellar
        return context
        

# InCellar
class CreateInCellar(LoginRequiredMixin, CreateView):
    """ Created incellar. """

    template_name = 'inventory/cellarglobal/incellar/create_incellar.html'
    model = InCellar
    pk_url_kwarg = 'id'
    fields = ['article', 'amount', 'description']
    success_url = reverse_lazy('inventory:list_cellar_global')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add supplie article to context."""
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        query_article = Supplie.objects.get(id=id)
        context['article'] = query_article
        return context


class ListViewInCellar(LoginRequiredMixin, ListView):
    """ Incellar all view. """

    template_name = 'inventory/cellarglobal/incellar/list_incellar.html'
    pk_url_kwarg = 'id'
    paginate_by = 15
    context_object_name = 'incellar'  

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """ Returns the list of the article, obtained by the id. """

        id = self.kwargs.get("id")
        queryset = InCellar.objects.filter(article__id=id)
       
        data_start = self.request.GET.get('start')
        data_end = self.request.GET.get('end')
        
        try:
            if data_start:
                data_start=datetime.datetime.strptime(data_start,'%Y-%m-%d').date()
                if data_end:
                    data_end=datetime.datetime.strptime(data_end,'%Y-%m-%d').date()
        except:
            data_start = None 
            data_end = None

       
        if data_start and data_end:
            queryset = queryset.filter(date__date__range= [data_start, data_end])

        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        article = get_object_or_404(CellarGlobal, article__id=id)
        context["article"] = article
        return context      
  

# OutCellar
class CreateOutCellar(LoginRequiredMixin, CreateView):
    """ create outcellar """

    template_name = 'inventory/cellarglobal/outcellar/create_outcellar.html'
    model = OutCellar
    pk_url_kwarg = 'id'
    fields = ['article', 'amount', 'description']
    success_url = reverse_lazy('inventory:list_cellar_global')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add supplie article to context."""
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        query_article = Supplie.objects.get(id=id)
        context['article'] = query_article
        return context


class ListViewOutCellar(LoginRequiredMixin, ListView):
    """ outcellar all view. """

    template_name = 'inventory/cellarglobal/outcellar/list_outcellar.html'
    pk_url_kwarg = 'id'
    paginate_by = 15
    context_object_name = 'outcellar'  

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs) 

    def get_queryset(self):
        id = self.kwargs.get("id")
        queryset = OutCellar.objects.filter(article__id=id)

        data_start = self.request.GET.get('start')
        data_end = self.request.GET.get('end')
        
        try:
            if data_start:
                data_start=datetime.datetime.strptime(data_start,'%Y-%m-%d').date()
                if data_end:
                    data_end=datetime.datetime.strptime(data_end,'%Y-%m-%d').date()
        except:
            data_start = None 
            data_end = None

       
        if data_start and data_end:
            queryset = queryset.filter(date__date__range= [data_start, data_end])
       
        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        article = get_object_or_404(CellarGlobal, article__id=id)
        context["article"] = article
        return context    


# RoomSpa
class CreatedRoomSpa(LoginRequiredMixin, CreateView):
    """ reate roomspa """

    template_name = 'inventory/roomspa/create_roomspa.html'
    model = RoomSpa
    fields = ['name', 'stretcher']
    success_url = reverse_lazy('inventory:list_roomspa')  

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

  
class UpdateRoomSpa(LoginRequiredMixin, UpdateView):
    """roomspa update"""

    template_name = 'inventory/roomspa/update_roomspa.html'
    pk_url_kwarg = 'id'
    model = RoomSpa
    fields = ['name', 'stretcher', 'condition']
    success_url = reverse_lazy('inventory:list_roomspa')
    
    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

class ListViewRoomSpa(LoginRequiredMixin, ListView):
    """ Roomspa all view. """

    template_name = 'inventory/roomspa/list_roomspa.html'
    paginate_by = 30
    context_object_name = 'roomspa'

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Update values 
        item_reload = ItemCleaningRoom.objects.all()
        for i in item_reload:
            i.save()
        
        data_search = self.request.GET.get('search')
        queryset = RoomSpa.objects.all()
        if data_search:
            queryset = queryset.filter( Q(name__icontains = data_search) | Q(stretcher__icontains = data_search))
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cost_items_room = RoomSpa.objects.filter().annotate(id_room=Coalesce('pk', 'pk')).annotate(sum_cost=Sum('itemcleaningroom__price_amount')).values('id_room', 'sum_cost')       
        context["cost_items_room"] = cost_items_room
        return context    

    
# ItemCleaningRoom
class CreateItemCleaningRoom(LoginRequiredMixin, CreateView):
    """ Create itemroom """

    template_name = 'inventory/roomspa/itemroomspa/create_itemroom.html'
    model = ItemCleaningRoom
    form_class = FormCreateItemRoom

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """ check if the article in use """

        query_valid = ItemCleaningRoom.objects.filter(roomspa=self.kwargs.get("id"), article=form.data['article']).exists()
        if query_valid:
            self.extra_context = {'item_in_use': 'Article is alredy in use'}
            return super().form_invalid(form)
        self.object = form.save()    
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add room to context."""

        context = super().get_context_data(**kwargs)
        room= RoomSpa.objects.get(id=self.kwargs.get("id"))
        context['room'] = room
        return context

    def get_success_url(self):
        """Return to list itemroom."""

        id = self.kwargs.get("id")
        return reverse('inventory:list_item_roomspa', kwargs={'id': id})    


class DeleteItemCleaningRoom(LoginRequiredMixin, DeleteView):
    """ User detail view."""

    template_name = 'inventory/roomspa/itemroomspa/delete_itemroom.html'
    pk_url_kwarg = 'id'
    model = ItemCleaningRoom

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Return to list itemroom."""

        id = self.object.roomspa.id
        return reverse('inventory:list_item_roomspa', kwargs={'id': id})


class ListViewItemCleaningRoom(LoginRequiredMixin, ListView):
    """ itemroom all view. """

    template_name = 'inventory/roomspa/itemroomspa/list_itemroom.html'
    pk_url_kwarg = 'id'
    paginate_by = 30
    context_object_name = 'itemroom' 

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

        #Update item in room
        if data_update_amount and data_update_amount_id:
            item_room = get_object_or_404(ItemCleaningRoom, id=data_update_amount_id)
            item_room.amount = data_update_amount
            item_room.save() 
        queryset = ItemCleaningRoom.objects.filter(roomspa__id=id)
        if data_search:
            queryset = queryset.filter(article__article__icontains = data_search)
        return queryset  

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        roomspa = RoomSpa.objects.get(id=id)
        context['room'] = roomspa
        return context   
