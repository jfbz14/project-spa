from django import forms
from datetime import datetime, timedelta
from django.db.models import Q
#model
from administrator.models import AdminDateService
from service.models import Service
from client.models import ProfileClient
from .models import ServiceAditional, BookingSpa
from inventory.models import RoomSpa
   
class FormCreateBookingNext(forms.Form):
    """ Form model bookingspa """

    list_hours = forms.CharField(max_length=2)
    client = forms.CharField(max_length=25, )
    document_number = forms.CharField(max_length=25, )
    service = forms.CharField(max_length=25, )
    date_day = forms.DateField(widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-52 p-2 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'type': 'date'}))
    date_hour = forms.TimeField(widget=forms.TimeInput(format=('%H:%M'), attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-52 p-2 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'type': 'time'}))
        
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

    def clean(self):
        """ Validate hour enable """
        cleaned_data = super().clean()

        service = cleaned_data.get('service')
        date_hour = cleaned_data.get('date_hour')
        date_day = cleaned_data.get('date_day')
        document_number = cleaned_data.get('document_number')
        if date_day and date_hour and service:

            date_day_admin = AdminDateService.objects.get(name_day=date_day.strftime('%A'), condition=True)
            client = ProfileClient.objects.get(document_number=document_number)
            data_service =Service.objects.get(name=service)
            date_today = datetime.now() - timedelta(minutes=2)
            try:
                # We get the values ​​of the opening and closing time, the requested time and we join date and time
                date_full = datetime.strptime(date_day.__str__() + ' ' + date_hour.__str__(), '%Y-%m-%d %H:%M:%S')
                date_admin_start = datetime.strptime(date_day.__str__() + ' ' + date_day_admin.time_start.__str__(), '%Y-%m-%d %H:%M:%S')
                date_admin_end = datetime.strptime(date_day.__str__() + ' ' + date_day_admin.time_end.__str__(), '%Y-%m-%d %H:%M:%S')
                # We validate if the requested time has not passed
                if date_today > date_full:
                    raise forms.ValidationError({'date_hour': forms.ValidationError('invalid, past tense')})
                #  we validate the time is open   
                elif date_full < date_admin_start or date_full > date_admin_end or (date_full + timedelta(minutes=data_service.time_minutes) > date_admin_end):    
                    raise forms.ValidationError({'date_hour': forms.ValidationError('invalid time, not open')})       
            except ValueError:
                raise forms.ValidationError({'date_hour': forms.ValidationError('Error data')})

        if date_day and date_hour and service:

            #check if there are reservations that day
            booking_valid_count= BookingSpa.objects.filter(created__date=date_full.date()).filter(Q(position='Wait') | Q(position='Active')).count()
            room_count = RoomSpa.objects.filter(positon=True).count()#number of rooms
            booking = BookingSpa.objects.filter(created__date=date_full.date(), client=client).filter(Q(position='Wait') | Q(position='Active')).values('created', 'end_hour').order_by('created')
            date_full_end = date_full + timedelta(minutes=data_service.time_minutes)
            #Validates if the client is in the same one several times
            for time_booking in booking:

                created = datetime.strptime(time_booking['created'].astimezone().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                end_hour = datetime.strptime(time_booking['end_hour'].astimezone().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                range_time =[created,]

                while created < end_hour:
                    created = created + timedelta(minutes=1)
                    range_time.append(created)
                if date_full in range_time or date_full_end in range_time:
                    raise forms.ValidationError({'client': forms.ValidationError('The customer has that busy time')})


            if booking_valid_count >= room_count:
                #if reservations exceed the number of rooms, we filter your created hours
                booking = BookingSpa.objects.filter(created__date=date_full.date()).filter(Q(position='Wait') | Q(position='Active'))
                booking_count = 0
                data=[]

                date_full_end = date_full + timedelta(minutes=data_service.time_minutes)

                for time_booking in booking.values('created', 'end_hour').order_by('created'):

                    created = datetime.strptime(time_booking['created'].astimezone().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    end_hour = datetime.strptime(time_booking['end_hour'].astimezone().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    range_time =[created,]

                    while created < end_hour:
                        created = created + timedelta(minutes=1)
                        range_time.append(created)
                    if date_full in range_time or date_full_end in range_time:
                        booking_count += 1 
                        data_new = {'start_time': range_time[1], 'end_time' : range_time[-1]}
                        data.append(data_new)

                if booking_count >= room_count:
                    list_hour_valid = set()
                    count_after = 0
                    count_before = 0

                    #filter hour after free
                    for time in data:
                        date_full = time['end_time'] + timedelta(minutes=1)
                        date_full_end = date_full + timedelta(minutes=data_service.time_minutes)
                        booking = booking.filter(created__gte=date_full).order_by('created')
                        for time_booking in booking.values('created', 'end_hour'):
                            created = datetime.strptime(time_booking['created'].astimezone().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            end_hour = datetime.strptime(time_booking['end_hour'].astimezone().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

                            range_time =[created,]

                            while created < end_hour:
                                created = created + timedelta(minutes=1)
                                range_time.append(created)

                            if date_full in range_time or date_full_end in range_time:
                                count_after += 1 
                                
                        if count_after < room_count:
                            list_hour_valid.add(date_full)

                    #filter hour before free
                    for time in data:
                        date_full = time['start_time'] - timedelta(minutes=data_service.time_minutes + 1)
                        date_full_end = time['start_time'] - timedelta(minutes=1)
                        
                        booking = booking.filter(created__gte=date_full).order_by('created')
                        for time_booking in booking.values('created', 'end_hour'):
                            created = datetime.strptime(time_booking['created'].astimezone().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            end_hour = datetime.strptime(time_booking['end_hour'].astimezone().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

                            range_time =[created,]

                            while created < end_hour:
                                created = created + timedelta(minutes=1)
                                range_time.append(created)

                            if date_full in range_time or date_full_end in range_time:
                                count_before += 1 
                                
                        if count_before < room_count:
                            list_hour_valid.add(date_full)        
                            
                    list_hour_valid = sorted(list(list_hour_valid))     
                    list_hours = []
                    for hour in list_hour_valid: 
                        hour_end = hour + timedelta(minutes=data_service.time_minutes)
                        hour_index = list_hour_valid.index(hour)
                        if date_today > hour or hour_end > date_admin_end or hour < date_admin_start:
                            continue
                        else:
                            list_hours.append(hour.time().__format__('%H:%M'))    

                    raise forms.ValidationError({'list_hours': forms.ValidationError('Available time{}'.format(list_hours))})  
                return cleaned_data
            return cleaned_data
        raise forms.ValidationError({'client': forms.ValidationError('Field invalid.')})

        
    def save(self):
        """Create booking and model serviceaditional."""
        data = self.cleaned_data

        service = data['service']
        date_hour = data['date_hour']
        date_day = data['date_day']
        document_number = data['document_number']
        client = ProfileClient.objects.get(document_number=document_number)
        service =Service.objects.get(name=service)
        created = datetime.strptime(date_day.__str__() + ' ' + date_hour.__str__(), '%Y-%m-%d %H:%M:%S')

        create_booking=BookingSpa.objects.create(
                client=client, 
                created=created,
                time_service=0,
                )
        service_aditional=ServiceAditional.objects.create(
                bookingspa=create_booking, 
                name_service=service.name,
                time_minutes=service.time_minutes,
                price=service.price,
                commission_percentage=service.commission_percentage)
        create_booking.time_service+=service_aditional.time_minutes  
        create_booking.save()         


class FormUpdateDateTimeBooking(forms.ModelForm):
    """ Form model AdinDateService """

    class Meta:

        model = BookingSpa
        fields = ('created',)
        widgets = {
            'created' : forms.DateTimeInput(format=('%Y-%m-%d %H:%M:%S'),attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'type': 'datetime-local'}),
        }
        
    def clean_created(self):
        """ validate name service exists """

        created = self.cleaned_data['created']
        created = datetime.strptime(created.date().__str__() + ' ' + created.time().__str__(), '%Y-%m-%d %H:%M:%S')
        datetime_now = datetime.now() - timedelta(minutes=3)

        if created < datetime_now:
            raise forms.ValidationError('Time invalid. Validate that it is not past tense')
        return created   