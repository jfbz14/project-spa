from django.views.generic import UpdateView, ListView, CreateView, FormView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from datetime import datetime, timedelta
from django.db.models import Q, Count, Sum 
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect

#model
from .models import BookingSpa, ServiceAditional
from client.models import ProfileClient
from .forms import FormCreateBookingNext, FormUpdateDateTimeBooking
from service.models import Service, ItemService
from inventory.models import RoomSpa, OutCellar, ItemCleaningRoom, InCellar
from profile_user.models import ProfileUser
from administrator.models import Sale

#Booking
class ListViewBookingSpaGestion(LoginRequiredMixin, ListView):
    """ 
        BookingSpa all view. 
        all reservations for today
    """

    template_name = 'booking/list_booking_gestion.html'
    paginate_by = 12
    context_object_name = 'booking' 

    def dispatch(self, request, *args, **kwargs):
        time_now = datetime.now().date() - timedelta(days=1)
        """
            if the day is earlier. 
            if there are active reservations, it closes them as a sale. 
            if there are reservations as a wait, it cancels them. 
        """
        booking_all = BookingSpa.objects.filter(condition_pay = False , created__date__lte=time_now).filter(Q(position='Active') | Q(position='Finalized') | Q(position='Wait')).exists()
        if booking_all:
            booking_all = BookingSpa.objects.filter(condition_pay = False , created__date__lte= time_now).filter(Q(position='Active') | Q(position='Finalized') | Q(position='Wait'))
            for booking in booking_all:
                if booking.position == 'Finalized' or  booking.position == 'Active':
                    Sale.objects.create(bookingspa=booking, price=booking.total_price, created=booking.created)
                    booking.condition_pay = True
                    booking.position = 'Finalized'
                    booking.room.condition = True
                    booking.save() 
                if booking.position == 'Wait':
                    booking.position = 'Cancel'
                    booking.advance_price = 0
                    booking.balance = 0
                    booking.total_price = 0
                    booking.condition_pay = False
                    booking.save() 
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')            
        return super().dispatch(request, *args, **kwargs)
  
    def get_queryset(self):
        """validate search field, otherwise it returns the model"""
        # Update field advance price
        data_advance_price_id = self.request.GET.get('update_advance_price_id')
        data_advance_price = self.request.GET.get('update_advance_price')
        try:
            if data_advance_price and data_advance_price_id:
                data_advance_price = float(data_advance_price)
                booking = BookingSpa.objects.get(id=data_advance_price_id)
                booking.advance_price = data_advance_price
                booking.save()
        except:
            pass        
        
        # Update field discount if profile is valid
        data_update_discount_id = self.request.GET.get('update_discount_id')
        data_update_discount = self.request.GET.get('update_discount')
        try:
            if data_update_discount and data_update_discount_id:
                data_update_discount = float(data_update_discount)
                booking = BookingSpa.objects.get(id=data_update_discount_id)
                booking.discount = data_update_discount
                booking.save()
        except:
            pass  

        #if there are changes in the values, it is updated.
        queryset = BookingSpa.objects.filter(Q(position='Wait') | Q(position='Active'))
        for booking in  queryset:
            service_aditional = ServiceAditional.objects.filter(bookingspa=booking).values('price')
            total_price = float()
            for service_price in service_aditional:
                total_price += service_price['price']
            booking.total_price = total_price - booking.discount
            booking.save()
            booking.balance = booking.total_price - booking.advance_price
            booking.end_hour = booking.created + timedelta(minutes=booking.time_service)
            booking.save()

        data_search = self.request.GET.get('search')
        data_start = self.request.GET.get('start')
        try:
            if data_start:
                data_start = datetime.strptime(data_start,'%Y-%m-%d').date()
        except :
            print('invalid date')
            data_start = None   

        queryset = BookingSpa.objects.filter(Q(position='Wait') | Q(position='Active') | Q(position='Finalized', condition_pay=False))
        if data_search and data_start:
            queryset = queryset.filter(created__date=data_start).filter(Q(client__first_name__icontains=data_search) | Q(client__last_name__icontains=data_search))          
        elif data_search:
            queryset = queryset.filter(Q(client__first_name__icontains=data_search) | Q(client__last_name__icontains=data_search))          
        elif data_start:
            queryset = queryset.filter(created__date=data_start)  
        else:
            queryset = queryset.filter(created__date=datetime.now().date())            
        return queryset.order_by('created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_position = self.request.user.profileuser.position
        if profile_position == 'administrator':
            context['valid_discount'] = True
        service = ServiceAditional.objects.filter(position='Active')
        erroractive = self.request.GET.get('erroractive')
        if erroractive:
            context["erroractive"] = 'The service has not finished'
        context["service"] = service
        return context

         
class ListViewBookingSpaWaitGestion(LoginRequiredMixin, ListView):
    """ all bookings on hold """

    template_name = 'booking/list_booking_wait_gestion.html'
    paginate_by = 15
    context_object_name = 'booking_wait'

    def dispatch(self, request, *args, **kwargs):
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            booking_valid = BookingSpa.objects.filter(position='Active', profile=profile).exists()
            if booking_valid:
                booking_active = get_object_or_404(BookingSpa, position='Active', profile=profile)
                return redirect('booking:detail_bookingactivate', id=booking_active.pk)
        return super().dispatch(request, *args, **kwargs)    

    def get_queryset(self):
        """validate search field, otherwise it returns the model"""

        date_now = datetime.now().date()
        query_filter_position = BookingSpa.objects.filter(position='Wait', created__date=date_now)

        data_search = self.request.GET.get('search')  
        if data_search:
            query_filter_position = query_filter_position.filter(Q(client__first_name__icontains=data_search) | Q(client__last_name__icontains=data_search))

        return query_filter_position 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        erroractive = self.request.GET.get('erroractive')
        if erroractive:
            context["erroractive"] = 'it is not time yet'
        service = ServiceAditional.objects.filter(position='Active', bookingspa__position ='Wait')
        context["service"] = service
        return context         


class ListViewBookingSpaActiveGestion(LoginRequiredMixin, ListView):
    """ BookingSpa all view. """

    template_name = 'booking/list_booking_active_gestion.html'
    paginate_by = 12
    context_object_name = 'booking_active'

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """validate search field, otherwise it returns the model"""

        query_filter_position = BookingSpa.objects.filter(position='Active')
        data_search = self.request.GET.get('search')
        if data_search:
            query_filter_position = query_filter_position.filter(Q(client__first_name__icontains=data_search) | Q(client__last_name__icontains=data_search)).distinct()
        return query_filter_position 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_all = ServiceAditional.objects.filter(position='Active', bookingspa__position ='Active')

        filter_time_service = ServiceAditional.objects.filter(
            position='Active', 
            bookingspa__position ='Active'
            ).annotate(booking=Coalesce('bookingspa__pk','bookingspa' )).values(
                'booking', 'bookingspa__active'
                ).annotate(total_time=Sum('time_minutes'))
        hour_end_booking = []
        for time in filter_time_service:
            time_minutes = timedelta(minutes=time['total_time'])
            time_end = time['bookingspa__active'] + time_minutes
            hour_end_booking.append({'booking': time['booking'], 'hour_end': time_end})
        context["service"] = service_all
        context["time_end"] = hour_end_booking
        return context    


class CancelBookindSpa(LoginRequiredMixin, UpdateView):
    """ Update booking position cancel """

    template_name = 'booking/cancel_booking.html'
    pk_url_kwarg = 'id'
    model = BookingSpa
    fields = ['position', 'description']

    def dispatch(self, request, *args, **kwargs):

        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        if booking.position == 'Cancel' or booking.position == 'Finalized':
            return redirect('booking:list_booking_gestion')
        
        profile = self.request.user.profileuser 
        if profile.position == 'administrator' or profile.position == 'assistant':
            return super().dispatch(request, *args, **kwargs)

        return redirect('booking:list_booking_gestion')

    def form_valid(self, form):

        valid_description = self.request.POST['description']

        if valid_description == 'None' or valid_description == '':
            self.extra_context = {'description_error' : 'Enter reason to cancel'} 
            return super().form_invalid(form)

        if len(valid_description) > 10:
            self.object = form.save()
            return super().form_valid(form)
        self.extra_context = {'description_error' : 'Enter reason to cancel'} 
        return super().form_invalid(form)
        
    def get_success_url(self):
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        booking.position = 'Cancel'
        booking.advance_price = 0
        booking.balance = 0
        booking.total_price = 0
        booking.time_service = 0
        booking.condition_pay = False
        booking.save()
        service_aditional = ServiceAditional.objects.filter(bookingspa=booking, position='Active').exists()
        if service_aditional:
            service_aditional = ServiceAditional.objects.filter(bookingspa=booking, position='Active')
            for service in service_aditional:
                service.price = 0
                service.position = 'Cancel'
                service.save()

        return reverse('booking:list_booking_gestion')


class CancelServiceAditionalBookingSpa(LoginRequiredMixin, UpdateView):
    """ Update the service aditional in position to cancel """   

    template_name = 'booking/cancel_serviceaditional_gte.html'
    pk_url_kwarg ='id'
    model = ServiceAditional
    fields = ['position']

    def dispatch(self, request, *args, **kwargs):
        id=self.kwargs['id']
        service_aditional = get_object_or_404(ServiceAditional, id=id)

        booking = get_object_or_404(BookingSpa, id=service_aditional.bookingspa.pk)
        if booking.position == 'Cancel' or booking.position == 'Finalized':
            return redirect('booking:list_booking_gestion')
        
        profile = self.request.user.profileuser 
        if profile.position == 'administrator' or profile.position == 'assistant':
            return super().dispatch(request, *args, **kwargs)

        return redirect('booking:list_booking_gestion')

    def form_valid(self, form):

        id=self.kwargs['id']
        service_aditional = get_object_or_404(ServiceAditional, id=id)
        booking = service_aditional.bookingspa
        if booking.position == 'Wait' or booking.position == 'Active':
            self.object = form.save()
            booking.time_service = booking.time_service - service_aditional.time_minutes
            booking.save()
            return super().form_valid(form)
        self.extra_context = {'cancel_error' : 'You can not delete service, booking is closed'} 
        return super().form_invalid(form)
    
    def get_success_url(self):

        id=self.kwargs['id']
        service_aditional = get_object_or_404(ServiceAditional, id=id)
        service_aditional.price = 0
        service_aditional.save()

        service = get_object_or_404(Service, name=service_aditional.name_service)

        if service_aditional.bookingspa.position == 'Active':
            item_service_valid = ItemService.objects.filter(service=service).exists
            if item_service_valid:
                item_service = ItemService.objects.filter(service=service)
                for item in item_service:
                    InCellar.objects.create(article=item.article,amount=item.amount, description= 'cancel service booking #{}'.format(service_aditional.bookingspa.pk))                  
        
        return reverse('booking:list_booking_gestion')


class CreateServiceAditionalBooking(LoginRequiredMixin, View):
    """ Create service aditional in booking wait or active """

    def dispatch(self, request, *args, **kwargs):
        booking_id = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        time_now = datetime.now().date()

        if time_now > booking_id.created.date():
            return redirect('booking:list_booking_gestion')

        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')

        return super().dispatch(request, *args, **kwargs)        

    def get(self, request, *args, **kwargs):

        name_service = Service.objects.all().values('name')
        booking_id = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        context = {
            'service' : name_service,
            'booking' : booking_id
        }
        
        return render (request, 'booking/create_serviceaditional_gte.html', context )  

    def post (self, request, *args, **kwargs):
        """ create sericeaditional in booking """   

        name_service = self.request.POST['service']
        id_bookingspa = self.request.POST['bookingspa']

        service_name = Service.objects.all().values('name')
        booking_id = get_object_or_404(BookingSpa, id=id_bookingspa)

        if name_service == 'None':
            """ valid if field is """

            context = {
                'service' : service_name,
                'booking' : booking_id,
                'service_error' : 'Select a service'
            }
            return render (request, 'booking/create_serviceaditional_gte.html', context )  
        
        if request.method == 'POST':
            """ Create service aditional """

            valid_id_booking = BookingSpa.objects.filter(id=id_bookingspa).exists()
            valid_service = Service.objects.filter(name=name_service).exists()
            
            if valid_id_booking and valid_service:

                service = get_object_or_404(Service, name=name_service)

                create_service = ServiceAditional.objects.create(
                    bookingspa = booking_id,
                    name_service = service.name,
                    time_minutes = service.time_minutes,
                    price = service.price,
                    commission_percentage = service.commission_percentage,
                )
                booking_id.time_service += create_service.time_minutes
                booking_id.save()
                if booking_id.position == 'Active':

                    valid_item_service = ItemService.objects.filter(service=service).exists()
                    if valid_item_service:
                        item_service = ItemService.objects.filter(service=service)

                        for item in item_service:
                            OutCellar.objects.create(article=item.article,amount=item.amount, description= 'booking #{}'.format(booking_id.id))                  

                return redirect ('booking:list_booking_gestion')
            else :
                context = {
                'service' : service_name,
                'booking' : booking_id,
                'service_error' : 'Select a service'
                }
            return render (request, 'booking/create_serviceaditional_gte.html', context )         

        context = {
            'service' : service_name,
            'booking' : booking_id,
            'service_error' : 'Select a service'
        }
        return render (request, 'booking/create_serviceaditional_gte.html', context )         


class UpdateBookingPositionActive(LoginRequiredMixin, View):
    """ change wait state to active state, discount room supplies and inventory supplies. """

    def dispatch(self, request, *args, **kwargs):

        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            booking_valid = BookingSpa.objects.filter(position='Active', profile=profile).exists()
            if booking_valid:
                booking_active = get_object_or_404(BookingSpa, position='Active', profile=profile)
                return redirect('booking:detail_bookingactivate', id=booking_active.pk)

        time_now = datetime.now() + timedelta(minutes=5)
        id_booking = self.kwargs['id_booking']
        booking = get_object_or_404(BookingSpa, id=id_booking)
        hour_booking = booking.created.astimezone()       

        # If it's not time to activate
        if time_now.strftime('%Y-%m-%d %H:%M') >= hour_booking.strftime('%Y-%m-%d %H:%M'):
            return super().dispatch(request, *args, **kwargs)
        url = "%s?erroractive=1" % reverse('booking:list_booking_wait_gestion')    
        return redirect(url) 

    def get(self, request, *args, **kwargs):

        id_booking = self.kwargs['id_booking']
        id_employee = self.kwargs['id_employee']
        employee = get_object_or_404(ProfileUser, id=id_employee)
        booking = get_object_or_404(BookingSpa, id=id_booking)
        # Valid if room available
        room_valid  = RoomSpa.objects.filter(condition=True).exists()
        # Valid if service is active
        service_aditional_valid = ServiceAditional.objects.filter(bookingspa=booking, position='Active').exists()

        if room_valid == False:

            context = {
                'room_valid' : room_valid,
                'service_valid' : service_aditional_valid,
                'employee' : employee,
                'booking' : booking

            }
            return render (request, 'booking/active_booking.html', context )

        room_name = RoomSpa.objects.filter(condition=True)

        if service_aditional_valid == False:
            context = {
                'room_valid' : room_valid,
                'service_valid' : service_aditional_valid,
                'room_name' : room_name,
                'employee' : employee,
                'booking' : booking

            }
            return render (request, 'booking/active_booking.html', context )

        service_aditional =  ServiceAditional.objects.filter(bookingspa=booking, position='Active')
        context = {
                'room_valid' : room_valid,
                'service_valid' : service_aditional_valid,
                'employee' : employee,
                'booking' : booking,
                'room_name' : room_name,
                'service' : service_aditional
            }
        return render (request, 'booking/active_booking.html', context )         


    def post(self, request, *args, **kwargs):
        """ 
            -Update condition from employee to occupied 
            -output of supplies the items services and intem clean room
            -Update position the booking to active
            -Update room to false 
        """
        id_booking = self.kwargs['id_booking']
        id_employee = self.kwargs['id_employee']
        id_room = self.request.POST['id_room']
        employee = get_object_or_404(ProfileUser, id=id_employee)
        booking = get_object_or_404(BookingSpa, id=id_booking)
        service_aditional_valid = ServiceAditional.objects.filter(bookingspa=booking, position='Active').exists()        
        service_aditional =  ServiceAditional.objects.filter(bookingspa=booking, position='Active')

        if id_room == 'None':
                
            room_valid  = RoomSpa.objects.filter(condition=True).exists()
            room_name = RoomSpa.objects.filter(condition=True)
            context = {
                'room_valid' : room_valid,
                'service_valid' : service_aditional_valid,
                'employee' : employee,
                'booking' : booking,
                'room_name' : room_name,
                'service' : service_aditional,
                'room_error' : 'Select to room',
            }
            return render (request, 'booking/active_booking.html', context )         

        room = get_object_or_404(RoomSpa, id=id_room)
        if request.method == 'POST':

            employee.condition = 'occupied'
            employee.save()
            room.condition = False
            room.save()
            booking.position = 'Active'
            booking.profile = employee
            booking.room = room
            booking.active = datetime.now()
            booking.save()

            item_service_aditional = ServiceAditional.objects.filter(bookingspa=booking, position='Active').exists()
            if item_service_aditional:
                item_service_aditional = ServiceAditional.objects.filter(bookingspa=booking, position='Active')

                for bookingspa in item_service_aditional:
                    service = get_object_or_404(Service, name=bookingspa.name_service)
                    item_service_valid = ItemService.objects.filter(service=service).exists
                    if item_service_valid:
                        item_service = ItemService.objects.filter(service=service)
                        for item in item_service:
                            OutCellar.objects.create(article=item.article,amount=item.amount, description= 'booking #{}'.format(booking.id))                  
            item_cleaning_room_valid = ItemCleaningRoom.objects.filter(roomspa=room).exists()
            if item_cleaning_room_valid:
                item_cleaning_room = ItemCleaningRoom.objects.filter(roomspa=room)

                for item in item_cleaning_room:
                    OutCellar.objects.create(article=item.article,amount=item.amount, description= 'booking #{}'.format(booking.id))                  

            return redirect ('booking:detail_bookingactivate', id=booking.pk)

        room_valid  = RoomSpa.objects.filter(condition=True).exists()
        room_name = RoomSpa.objects.filter(condition=True)
        context = {
            'room_valid' : room_valid,
            'employee' : employee,
            'booking' : booking,
            'room_name' : room_name,
            'room_error' : 'Select to room',
        }
        return render (request, 'booking/active_booking.html', context ) 


class DetailBookingActivate(LoginRequiredMixin, DetailView):
    """ View the booking in condition activate """

    template_name = 'booking/detail_bookingactivate.html'
    pk_url_kwarg = 'id'
    model = BookingSpa

    def dispatch(self, request, *args, **kwargs):
        
        profile = self.request.user.profileuser 
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])

        if booking.position == 'Active':
            if profile == booking.profile or profile.position == 'administrator' or profile.position == 'assistant':

                return super().dispatch(request, *args, **kwargs)

        return redirect('booking:list_booking_active_gestion')  
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        service = ServiceAditional.objects.filter(bookingspa=booking.pk, position='Active')
        finalize_time = booking.active.astimezone() + timedelta(minutes=booking.time_service)    

        context["service"] = service
        context['finalize_time'] = finalize_time

        return context
    
    
class AddServiceAditionalBookingActive(LoginRequiredMixin, View):
    """ Create service aditional in booking active """

    def dispatch(self, request, *args, **kwargs):
        id_bookingspa = self.kwargs['id']
        booking = get_object_or_404(BookingSpa, id=id_bookingspa)

        if booking.position == 'Cancel' or booking.position == 'Finalized':
            return redirect ('booking:list_booking_gestion')

        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):

        name_service = Service.objects.all().values('name')
        booking_id = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        context = {
            'service' : name_service,
            'booking' : booking_id
        }
        
        return render (request, 'booking/add_serviceaditional_gte.html', context )  

    def post (self, request, *args, **kwargs):
        """ create sericeaditional in booking """   

        name_service = self.request.POST['service']
        id_bookingspa = self.request.POST['bookingspa']

        service_name = Service.objects.all().values('name')
        booking_id = get_object_or_404(BookingSpa, id=id_bookingspa)

        if name_service == 'None':
            """ valid if field is """

            context = {
                'service' : service_name,
                'booking' : booking_id,
                'service_error' : 'Select a service'
            }
            return render (request, 'booking/add_serviceaditional_gte.html', context )  
        
        if request.method == 'POST':
            """ Create service aditional """

            valid_id_booking = BookingSpa.objects.filter(id=id_bookingspa).exists()
            valid_service = Service.objects.filter(name=name_service).exists()
            
            if valid_id_booking and valid_service:

                service = get_object_or_404(Service, name=name_service)

                create_service = ServiceAditional.objects.create(
                    bookingspa = booking_id,
                    name_service = service.name,
                    time_minutes = service.time_minutes,
                    price = service.price,
                    commission_percentage = service.commission_percentage,
                )
                booking_id.time_service += create_service.time_minutes
                booking_id.save()

                if booking_id.position == 'Active':

                    valid_item_service = ItemService.objects.filter(service=service).exists()
                    if valid_item_service:
                        item_service = ItemService.objects.filter(service=service)

                        for item in item_service:
                            OutCellar.objects.create(article=item.article,amount=item.amount, description= 'booking #{}'.format(booking_id.id))                  

                queryset = BookingSpa.objects.filter(Q(position='Wait') | Q(position='Active'))
                for booking in  queryset:
                    service_aditional = ServiceAditional.objects.filter(bookingspa=booking).values('price')
                    total_price = float()
                    for service_price in service_aditional:
                        total_price += service_price['price']
                    booking.total_price = total_price
                    booking.save()
                    booking.balance = booking.total_price -booking.advance_price- booking.discount
                    booking.save()

                return redirect ('booking:detail_bookingactivate' , id=id_bookingspa)
            else :
                context = {
                'service' : service_name,
                'booking' : booking_id,
                'service_error' : 'Select a service'
                }
            return render (request, 'booking/add_serviceaditional_gte.html', context )         

        context = {
            'service' : service_name,
            'booking' : booking_id,
            'service_error' : 'Select a service'
        }
        return render (request, 'booking/add_serviceaditional_gte.html', context )  


class UpdateViewDateTimeBooking(LoginRequiredMixin, UpdateView):
    """ Update field datetiem booking in position Wait """

    template_name = 'booking/update_datetime_booking.html'
    pk_url_kwarg = 'id'
    model = BookingSpa
    form_class = FormUpdateDateTimeBooking
    success_url = reverse_lazy('booking:list_booking_gestion')

    def dispatch(self, request, *args, **kwargs):
        id=self.kwargs['id']
        booking = get_object_or_404(BookingSpa, id=id)
        if booking.position == 'Wait':
            profile = self.request.user.profileuser 
            if profile.position == 'administrator' or profile.position == 'assistant':

                return super().dispatch(request, *args, **kwargs)
            return redirect('booking:list_booking_gestion')

        return redirect('booking:list_booking_gestion')
    

class FinalizedBookindSpa(LoginRequiredMixin, UpdateView):
    """ Update booking finalized """

    template_name = 'booking/finalized_serviceaditional_gte.html'
    pk_url_kwarg = 'id'
    model = BookingSpa
    fields = ['position']

    def dispatch(self, request, *args, **kwargs):
        
        profile = self.request.user.profileuser 
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])

        if profile == booking.profile or profile.position == 'administrator' or profile.position == 'assistant':

            return super().dispatch(request, *args, **kwargs)

        return redirect('booking:detail_bookingactivate', id=self.kwargs['id'])

    def get_success_url(self):
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        booking.position = 'Finalized'
        booking.end_booking = datetime.now()
        booking.save()
        room = booking.room
        room.condition = True
        room.save()
        employee = booking.profile
        employee.condition = 'activated'
        employee.save()

               
        return reverse('booking:list_booking_wait_gestion')   


class ListBookingSpaWait(LoginRequiredMixin, ListView):
    """ View BookingSpa all wait. """

    template_name = 'booking/list_bookingspa_wait_all.html'
    paginate_by = 15

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        data_start = self.request.GET.get('start')
        data_search = self.request.GET.get('search')

        try:
            if data_start:
                data_start=datetime.strptime(data_start,'%Y-%m-%d').date()
        except:
            data_start = None      

        queryset=BookingSpa.objects.filter(position='Wait').annotate(count_service=Count('serviceaditional', filter=Q(serviceaditional__position='Active')))
               
        if data_start and data_search:
            queryset = queryset.filter(created__date=data_start, id=data_search)

        elif data_start:     
            queryset = queryset.filter(created__date=data_start)
        
        elif data_search:
            queryset = queryset.filter(id=data_search) 

        else:
            queryset = queryset.filter(created__date__gte=datetime.now().date())     
  
        return queryset.order_by('created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service"] = ServiceAditional.objects.filter(position='Active')
        return context


class CreateSaleBooking(LoginRequiredMixin, CreateView):
    """ create model Sale """  

    template_name = 'administrator/sale/create_sale_booking.html'
    pk_url_kwarg = 'id'
    model = Sale
    fields = ['bookingspa', 'payment_method', 'price', 'assistant', 'created']

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        if booking.position == 'Finalized':
            return super().dispatch(request, *args, **kwargs)
        url = "%s?erroractive=1" % reverse('booking:list_booking_gestion')    
        return redirect(url)     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        context["booking"] = booking
        context["datetime_sale"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return context
         
    def get_success_url(self):
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        booking.condition_pay = True
        booking.save()
        return reverse('booking:list_booking_gestion')     
    

class CreateBooking(LoginRequiredMixin, ListView):
    """ Create Booking """

    template_name = 'booking/create_booking.html'

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        data_search = self.request.GET.get('search')
        queryset = {}
        if data_search:   
            queryset = ProfileClient.objects.filter(Q(document_number__icontains = data_search) | Q(first_name__icontains = data_search) | Q(last_name__icontains = data_search)).distinct()

        return queryset


class CreateBookingNext(LoginRequiredMixin, FormView):
    """ Continue with the creation of booking """

    template_name = 'booking/create_booking_next.html'
    form_class = FormCreateBookingNext
    success_url = reverse_lazy('booking:list_booking_gestion')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service"] = Service.objects.all().values('name')
        context["client"] = get_object_or_404(ProfileClient, id=self.kwargs['id'])
        return context

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)
   
