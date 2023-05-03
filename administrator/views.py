from django.views.generic import UpdateView, ListView, FormView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from datetime import datetime, timedelta
from django.db.models import Q, Count, Sum 
from django.db.models.functions import TruncDay, Coalesce
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from easy_pdf.views import PDFTemplateView

#model
from administrator.models import Expenses, Sale, AdminDateService, EmployeeHistoryBooking, ServiceEmployeeBooking, CompanyData, FixedCosts
from administrator.forms import FormCreateExpense, FormUpdateAdminDateService, FormCreateFixedCosts
from service.models import Service
from profile_user.models import ProfileUser
from booking.models import BookingSpa, ServiceAditional

#Expenses

class CreateExpense(LoginRequiredMixin, FormView):
    """ create expense """

    template_name = 'administrator/expense/create_expense.html'
    form_class = FormCreateExpense
    success_url = reverse_lazy('administrator:list_expense')

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


class ListViewExpenses(LoginRequiredMixin, ListView):
    """ list views all expese"""

    template_name = 'administrator/expense/list_expense.html'
    paginate_by = 15
    context_object_name = 'expense'

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """validate search field, otherwise it returns the model"""
                
        data_search = self.request.GET.get('search')
        data_start = self.request.GET.get('start')
        data_end = self.request.GET.get('end')

        try:
            if data_start:
                data_start=datetime.strptime(data_start,'%Y-%m-%d').date()
                if data_end:
                    data_end=datetime.strptime(data_end,'%Y-%m-%d').date()
        except:
            data_start = None 
            data_end = None  

        queryset = Expenses.objects.all()   
        
        if data_start and  data_end and data_search:
            queryset = queryset.filter(created__range=[data_start, data_end], classsification=data_search)
        elif data_start and  data_end:
            queryset = queryset.filter(created__range=[data_start, data_end])
        elif data_start:
            queryset = queryset.filter(created__gte=data_start)
        elif  data_end:
            queryset = queryset.filter(created__lte=data_end)
        elif data_search:
            queryset = queryset.filter(classsification=data_search)

        price_total_query = queryset.values('price_total')
        price_total = float()
        for price in price_total_query:
           price_total += price['price_total']   

        self.extra_context = {'price_total':price_total}

        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return queryset.order_by('-created')
        return queryset.order_by('-created').exclude(is_valid=True)


class UpdateExpense(LoginRequiredMixin, UpdateView):
    """ Update Expense """

    template_name = 'administrator/expense/update_expense.html'
    pk_url_kwarg = 'id'
    model = Expenses
    form_class = FormCreateExpense
    success_url = reverse_lazy('administrator:list_expense')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

# Fixed Costs

class CreateFixedCosts(LoginRequiredMixin, FormView):
    """ create fixed costs """

    template_name = 'administrator/expense/create_fixed_costs.html'
    form_class = FormCreateFixedCosts
    success_url = reverse_lazy('administrator:list_fixed_costs')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_wait_gestion')
    
    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


class ListViewFixedCosts(LoginRequiredMixin, ListView):
    """ list views all expese"""

    template_name = 'administrator/expense/list_fixed_costs.html'
    paginate_by = 15
    context_object_name = 'fixed_costs'

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_wait_gestion')

    def get_queryset(self):
        """validate search field, otherwise it returns the model"""
                
        data_search = self.request.GET.get('search')
        
        queryset = FixedCosts.objects.all()   
        
        if data_search:
            queryset = queryset.filter(description__icontains=data_search)

        try:
            price_total_query = queryset.values('price')
            price_total = float()
        
            for price in price_total_query:
                price_total += price['price']   
        except:
            price_total = 0    
           
        self.extra_context = {'price_total':price_total}
  
        return queryset


class UpdateFixedCosts(LoginRequiredMixin, UpdateView):
    """ Update Expense """

    template_name = 'administrator/expense/update_fixed_costs.html'
    pk_url_kwarg = 'id'
    model = FixedCosts
    form_class = FormCreateFixedCosts
    success_url = reverse_lazy('administrator:list_fixed_costs')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_wait_gestion')
    

class DeleteFixedCosts(LoginRequiredMixin, DeleteView):
    """ User detail view."""

    template_name = 'administrator/expense/delete_fixed_costs.html'
    pk_url_kwarg = 'id'
    model = FixedCosts
    success_url = reverse_lazy('administrator:list_fixed_costs')

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_wait_gestion')
    

#Date Admin
class UpdateAdminDateTime(LoginRequiredMixin, UpdateView):
    """ Create model admindatetime """
    
    template_name = 'administrator/admin/update_admindatetime.html'
    model = AdminDateService
    form_class = FormUpdateAdminDateService
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('administrator:list_admindatetime')

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


class ListAdminDateTime(LoginRequiredMixin, ListView):

    template_name = 'administrator/admin/list_admindatetime.html'
    model = AdminDateService
    context_object_name = 'list_date_admin'

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)


#Admin
class ListViewBookingSpa(LoginRequiredMixin, ListView):
    """ BookingSpa all view. """

    template_name = 'administrator/booking/list_bookingspa.html'
    paginate_by = 12
    context_object_name = 'booking' 

    def dispatch(self, request, *args, **kwargs):
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_gestion')
  
    def get_queryset(self):
        """validate search field, otherwise it returns the model"""
        
        queryset = BookingSpa.objects.filter(Q(position='Wait') | Q(position='Active'))
        for booking in  queryset:
            service_aditional = ServiceAditional.objects.filter(bookingspa=booking).values('price')
            total_price = float()
            for service_price in service_aditional:
                total_price += service_price['price']
            booking.total_price = total_price - booking.discount
            booking.save()
            booking.balance = booking.total_price - booking.advance_price
            booking.save()
        queryset = BookingSpa.objects.all().annotate(count_service=Count('serviceaditional')).annotate(count_service_cancel=Count('serviceaditional', filter=Q(serviceaditional__position='Cancel')))

        data_start = self.request.GET.get('start')
        data_search_id = self.request.GET.get('search_id')
        data_search = self.request.GET.get('search')

        try:
            if data_start:
                data_start=datetime.strptime(data_start,'%Y-%m-%d').date()
        except:
            data_start = None        
              
        if data_start and data_search_id and data_search :   
            queryset = queryset.filter(created__date=data_start, position=data_search, id=data_search_id)
                
        elif data_start and data_search_id:   
            queryset = queryset.filter(created__date=data_start, id=data_search_id)
            
        elif data_start and data_search:
            queryset = queryset.filter(created__date=data_start, position=data_search)

        elif data_search_id and data_search:
            queryset = queryset.filter(id=data_search_id, position=data_search)
        
        elif data_start:     
            queryset = queryset.filter(created__date=data_start)
        
        elif data_search_id:     
            queryset = queryset.filter(id=data_search_id)

        elif data_search:
            queryset = queryset.filter(position=data_search)
  
        return queryset.order_by('-created')

   
class ListServiceAditional(LoginRequiredMixin, ListView):
    """view of all reserve services"""

    template_name = 'administrator/booking/list_serviceaditional.html'
    pk_url_kwarg = 'id'
    paginate_by = 10
    context_object_name = 'list_service'

    def dispatch(self, request, *args, **kwargs):
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_gestion')    
    
    def get_queryset(self):
        id = self.kwargs.get("id")
        queryset = ServiceAditional.objects.filter(bookingspa=id)
        return queryset  

    def get_context_data(self, **kwargs):
        """Add id Booking at services."""

        context = super().get_context_data(**kwargs)
        query_bookingspa = BookingSpa.objects.get(id=self.kwargs.get("id"))
        context['booking'] = query_bookingspa
        return context   


class ListEmployeeServiceFinalized(LoginRequiredMixin, ListView):
    """ List all service employee """

    template_name = 'administrator/admin/list_employee_finalized.html' 
    paginate_by = 12
    model = EmployeeHistoryBooking

    def dispatch(self, request, *args, **kwargs):
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_gestion')

    def get_queryset(self):

        data_start = self.request.GET.get('start')
        data_profile = self.request.GET.get('search')

        try:
            if data_start:
                data_start=datetime.strptime(data_start,'%Y-%m-%d').date()
        except:
            data_start = None        

        queryset = EmployeeHistoryBooking.objects.all()
        if data_start and data_profile:
            queryset =  queryset.filter(created=data_start).filter(Q(profile__user__first_name__icontains = data_profile) | Q(profile__user__last_name__icontains = data_profile))  
        elif data_start:
            queryset =  queryset.filter(created=data_start)  
        elif data_profile:
            queryset =  queryset.filter(Q(profile__user__first_name__icontains = data_profile) | Q(profile__user__last_name__icontains = data_profile))  

        return queryset.order_by('-created')
 
        
class UpdateEmployeeHistoryService(LoginRequiredMixin, View):
    """ Update the history """

    def dispatch(self, request, *args, **kwargs):
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_gestion')

    def get(self, request, *args, **kwargs):

        time_now = datetime.now().date() - timedelta(days=1) #get day yesterday
        booking_date_valid = BookingSpa.objects.filter(created__date__lte=time_now).exists() 

        if booking_date_valid:
            employee_history_date = EmployeeHistoryBooking.objects.filter(created__lte=time_now).values('created')# get all date
            booking_date = BookingSpa.objects.filter(created__date__lte=time_now).values('created__date')# get all date 
            booking_date_set = set()
            for i in booking_date:
                booking_date_set.add(i['created__date'])
            employee_history_date_set = set()
            for i in employee_history_date:
                employee_history_date_set.add(i['created'])    

            booking_date = booking_date_set
            employee_history_date = employee_history_date_set    
            missing_date = booking_date - employee_history_date
            missing_date = sorted(missing_date)
           
            if missing_date.__len__() >= 1:
                for date_create in missing_date:
                    
                    booking_all =BookingSpa.objects.filter(condition_pay=True, created__date=date_create)
                    booking_all = booking_all.annotate(day=TruncDay('created__date')).values('day').annotate(
                    profile=Coalesce('profile', 'profile'), 
                    count_booking=Count('condition_pay'))

                    for booking in booking_all:

                        serviceaditional = ServiceAditional.objects.filter(bookingspa__created__date=booking['day'], bookingspa__profile=booking['profile'], position='Active' )
                        day = AdminDateService.objects.get(name_day=booking['day'].strftime('%A'))
                        profile = ProfileUser.objects.get(id=booking['profile'])
                        history_employee = EmployeeHistoryBooking.objects.create(
                            created=booking['day'], 
                            profile=profile,
                            count_booking=booking['count_booking'],
                            count_service=serviceaditional.__len__(),
                            commission_limit = day.commission_limit
                            )
                        for service_aditional in serviceaditional:
                            service = Service.objects.get(name=service_aditional.name_service)
                            service_employee = ServiceEmployeeBooking.objects.create(
                                employee = history_employee,
                                name_service = service_aditional.name_service,
                                price = service_aditional.price,
                                commission_percentage = service.commission_percentage,
                                total_commission = service_aditional.price * (service.commission_percentage / 100),
                                created = service_aditional.created,
                                id_booking = service_aditional.bookingspa.pk
                            )

        return redirect('administrator:list_employee_service')


class ListServiceHistoryemployee(LoginRequiredMixin, ListView):
    """ view all service active and booking True the profile """

    template_name = 'administrator/admin/list_employee_finalized_detail.html'
    pk_url_kwarg = 'id'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_gestion')

    def get_queryset(self):

        id_employeehistorybooking = self.kwargs['id']
        queryset=ServiceEmployeeBooking.objects.filter(employee=id_employeehistorybooking)
        return queryset.order_by('-created')


class ListSaleBooking(LoginRequiredMixin, ListView):
    """ List view all model sale """

    template_name = 'administrator/admin/list_sale_booking.html' 
    model = Sale
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        profile = self.request.user.profileuser.position
        if profile == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return reverse('administrator:list_booking_gestion')    

    def get_queryset(self):
                
        data_start = self.request.GET.get('start')
        data_search = self.request.GET.get('search')

        try:
            if data_start:
                data_start=datetime.strptime(data_start,'%Y-%m-%d').date()
        except:
            data_start = None 

        queryset = Sale.objects.all()    
            
        if data_start and data_search:
            queryset = queryset.filter(created__date=data_start, payment_method=data_search)
        
        elif data_start:     
            queryset = queryset.filter(created__date=data_start)
        
        elif data_search:
            queryset = queryset.filter(payment_method=data_search)

        # Return value total    
        sales = queryset.values('price')
        total_sale = float()
        for sale in sales:
            total_sale += sale['price']   
        self.extra_context = {'total_sale':total_sale}
  
        return queryset.order_by('-created')


class ListBookingSpaSaleTrue(LoginRequiredMixin, ListView):
    """ List all booking sale condition pay is True """

    template_name = 'administrator/admin/list_booking_sale_true.html'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        # validates if you have permission for the view            
        profile = self.request.user.profileuser
        if profile.position == 'masseur':
            return redirect('booking:list_booking_wait_gestion')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        data_start = self.request.GET.get('start')
        data_search = self.request.GET.get('search')
        data_search_method = self.request.GET.get('search_method')

        try:
            if data_start:
                data_start=datetime.strptime(data_start,'%Y-%m-%d').date()
        except:
            data_start = None 

        queryset = BookingSpa.objects.filter(condition_pay=True).annotate(count_service=Count('serviceaditional', filter=Q(serviceaditional__position='Active')))              
            
        if data_start and data_search_method:
            queryset = queryset.filter(created__date=data_start, sale__payment_method=data_search_method)

        elif data_start and data_search:
            queryset = queryset.filter(created__date=data_start, id=data_search)  

        elif data_search_method:
            queryset = queryset.filter(sale__payment_method=data_search_method)    

        elif data_start:     
            queryset = queryset.filter(created__date=data_start)

        elif data_search:
            queryset = queryset.filter(id=data_search)  

         # Return value total    
        sales = queryset.values('total_price')
        total_sale = float()
        for sale in sales:
            total_sale += sale['total_price']   
        self.extra_context = {'total_sale':total_sale}

        return queryset.order_by('-created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service"] = ServiceAditional.objects.filter(position='Active')
        return context
    

class ListDashBoard(LoginRequiredMixin, ListView):

    template_name = 'administrator/admin/list_dashboard.html' 
    context_object_name = 'booking'

    def dispatch(self, request, *args, **kwargs):
        profile = self.request.user.profileuser
        if profile.position == 'administrator':
            return super().dispatch(request, *args, **kwargs)
        return redirect('booking:list_booking_gestion')

    def get_queryset(self):

        data_start = self.request.GET.get('start')
        data_end = self.request.GET.get('end')
        
        try:
            if data_start:
                data_start=datetime.strptime(data_start,'%Y-%m-%d').date()
                if data_end:
                    data_end=datetime.strptime(data_end,'%Y-%m-%d').date()
        except:
            data_start = None 
            data_end = None

        sale_all = Sale.objects.all()
        expense_all = Expenses.objects.all()
        queryset_bookingspa = BookingSpa.objects.all()
        query_service_serviceaditional = ServiceAditional.objects.all()

        if data_start and data_end:
            sale_all = sale_all.filter(created__date__range=[data_start, data_end]) 
            expense_all = expense_all.filter(created__range=[data_start, data_end])
            queryset_bookingspa = queryset_bookingspa.filter(created__date__range=[data_start, data_end]) 
            query_service_serviceaditional = query_service_serviceaditional.filter(created__date__range=[data_start, data_end])

        elif data_start:
            sale_all = sale_all.filter(created__date_gte=data_start) 
            expense_all = expense_all.filter(created_gte=data_start)
            queryset_bookingspa = queryset_bookingspa.filter(created__date_gte=data_start) 
            query_service_serviceaditional = query_service_serviceaditional.filter(created__date_gte=data_start)

        elif data_end:
            sale_all = sale_all.filter(created__date_lte=data_end) 
            expense_all = expense_all.filter(created_lte=data_end)
            queryset_bookingspa = queryset_bookingspa.filter(created__date_lte=data_end) 
            query_service_serviceaditional = query_service_serviceaditional.filter(created__date_lte=data_end)

        else:
            sale_all = sale_all.filter(created__date__month=datetime.now().month)    
            expense_all = expense_all.filter(created__month=datetime.now().month) 
            queryset_bookingspa = queryset_bookingspa.filter(created__date__month=datetime.now().month) 
            query_service_serviceaditional = query_service_serviceaditional.filter(created__date__month=datetime.now().month)

        # Query sale
        sale_all_filter = sale_all.annotate(day=TruncDay('created__date')).values('day').annotate(sum_sale=Sum('price')).order_by('day')
        sum_sale = float()
        for sale in sale_all_filter:
            sum_sale += sale['sum_sale']  

        # Query Card 
        card_count = sale_all.filter(payment_method='Card').annotate(day=TruncDay('created__date')).values('day').annotate(sum_sale_card=Sum('price'))  
        sum_sale_card = float()
        for sale_card in card_count:
            sum_sale_card += sale_card['sum_sale_card']   

        # Query Cash 
        cash_count = sale_all.filter(payment_method='Cash').annotate(day=TruncDay('created__date')).values('day').annotate(sum_sale_cash=Sum('price'))  
        sum_sale_cash = float()
        for sale_cash in cash_count:
            sum_sale_cash += sale_cash['sum_sale_cash']   

        # Query Expense    
        expense_all = expense_all.annotate(day=TruncDay('created')).values('day').annotate(sum_expense=Sum('price_total')).order_by('day')
        sum_expense = float()
        for expense in expense_all:
            sum_expense += expense['sum_expense']     

        # Booking filter
        booking_cancel = queryset_bookingspa.filter(position='Cancel').count()
        booking_payment = queryset_bookingspa.filter(condition_pay=True).count()
        booking_count = queryset_bookingspa.count()
        booking_total_price = queryset_bookingspa.filter(condition_pay=True).annotate(day=TruncDay('created__date')).annotate(suma_total_price=Sum('total_price')).values('suma_total_price')
        total_price_all = float()
        for total in booking_total_price:
            total_price_all += total['suma_total_price']
        booking_total_price = total_price_all   

        service_cancel = query_service_serviceaditional.filter(position='Cancel').count()

        queryset = {
            'cancel' : booking_cancel,
            'payment' : booking_payment,
            'booking_count' : booking_count,
            'total_price' : booking_total_price,
            'service_cancel' : service_cancel,
            'sum_expense' : sum_expense,
            'sum_sale' : sum_sale,
            'sum_total' : sum_sale - sum_expense,
            'card_count' : sum_sale_card,
            'cash_count' : sum_sale_cash,
            
            }   
        self.extra_context = {'sale' : sale_all_filter,
                              'expense': expense_all,
                              }

        return queryset
 

class PdfView(LoginRequiredMixin, PDFTemplateView):
    """ Create pdf """

    template_name = 'administrator/admin/pdf_detail_booking.html'   

    def get_pdf_filename(self):        
        """
        Returns :attr:`pdf_filename` value by default.
        If left blank the browser will display the PDF inline.
        Otherwise it will pop up the "Save as.." dialog.
        :rtype: :func:`str`
        """
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        self.pdf_filename = 'Booking_N°{}.pdf'.format(booking.pk)

        return self.pdf_filename    

    def get_context_data(self, **kwargs):
        booking = get_object_or_404(BookingSpa, id=self.kwargs['id'])
        service = ServiceAditional.objects.filter(bookingspa=booking, position='Active')
        payment_method = get_object_or_404(Sale, bookingspa=booking)
        total_price_sevice = float()
        company = get_object_or_404(CompanyData, id=1)
        
        for price in service.values('price'):
            total_price_sevice += price['price']
        return super(PdfView, self).get_context_data(
            pagesize = 'A4',
            route = '{}{}'.format(settings.BASE_DIR, '/'),
            booking = booking,
            service = service,
            payment_method = payment_method,
            total_price_sevice = total_price_sevice,
            company = company,
            **kwargs
        )      
