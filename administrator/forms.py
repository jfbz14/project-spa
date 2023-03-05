from django import forms
from datetime import datetime

#model
from administrator.models import Expenses, AdminDateService, FixedCosts
from service.models import Service
from client.models import ProfileClient


class FormCreateExpense(forms.ModelForm):
    """ form model expense"""

    class Meta:

        model = Expenses
        fields = '__all__'
        widgets = {
            'created' : forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'type': 'date'}),
            'distributor' : forms.Select(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'number' : forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'price_total' : forms.NumberInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'description' : forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'classsification' : forms.Select(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'is_valid' : forms.Select(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
        }

    def clean_created(self):
        """ validate future date. """

        created = self.cleaned_data['created']
        date_today = datetime.now().date()

        if created > date_today:
            raise forms.ValidationError('invalid date, not future.')
        return created 


class FormCreateFixedCosts(forms.ModelForm):
    """ form model expense"""

    class Meta:

        model = FixedCosts
        fields = '__all__'
        widgets = {
            'description' : forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'distributor' : forms.Select(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'price' : forms.NumberInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),

        }   


class FormUpdateAdminDateService(forms.ModelForm):
    """ Form model AdinDateService """

    class Meta:

        model = AdminDateService
        fields = ('time_start', 'time_end', 'commission_limit', 'condition' )
        widgets = {
            'time_start' : forms.TimeInput(format=('%H:%M:%S'),attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'type': 'time'}),
            'time_end' : forms.TimeInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'type': 'time'}),
            'commission_limit' : forms.NumberInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'condition' : forms.CheckboxInput(attrs={'class':'w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'})
        }


    def clean_time_end(self):
        """ validate name service exists """

        time_end = self.cleaned_data['time_end']
        time_start = self.cleaned_data['time_start']

        if time_end < time_start:
            raise forms.ValidationError('Time end invalid.')
        return time_end

    
class FormCreateBookingStart(forms.Form):
    """ Form model bookingspa """

    document_number = forms.CharField(max_length=25, )
    service = forms.CharField(max_length=25, )
    date_day = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}))

        
    def clean_document_number(self):
        """validate document number the cleint, exists """

        document_number = self.cleaned_data['document_number']
        if document_number == 'None':
            raise forms.ValidationError('Select a Document .')

        document_number_taken = ProfileClient.objects.filter(document_number=document_number).exists()

        if document_number_taken == False:
            raise forms.ValidationError('the document number does not exist.')
        return document_number

    def clean_date_day(self):
        """validate old date or day enabled """

        date_day = self.cleaned_data['date_day']
        date_today = datetime.now().date()
        date_day_admin_confirmation = AdminDateService.objects.filter(name_day=date_day.strftime('%A'), condition=True).exists()
        if date_day < date_today:
            raise forms.ValidationError('invalid, old date.')
        elif date_day_admin_confirmation == False:
            raise forms.ValidationError('Date not enabled.')

        return date_day    
    
    def clean_service(self):
        """validate name service exists """

        service = self.cleaned_data['service']

        if service == 'None':
            raise forms.ValidationError('Select a service .')

        name_service_taken = Service.objects.filter(name=service).exists()

        if name_service_taken == False:
            raise forms.ValidationError('The service does not exist.')
        return service
    
  
