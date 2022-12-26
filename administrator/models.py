#django
from django.db import models

#model
from profile_user.models import ProfileUser
from inventory.models import Distributor
from phonenumber_field.modelfields import PhoneNumberField
from booking.models import BookingSpa


# Create your models here.

class AdminDateService(models.Model):
    """model datetime service"""

    CHOICES_DAYS =[
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        ('Sunday','Sunday'),
    ]

    name_day =models.CharField(max_length=25, choices=CHOICES_DAYS, unique=True)
    time_start = models.TimeField(help_text='HH:MM')
    time_end = models.TimeField(help_text='HH:MM')
    commission_limit = models.IntegerField(default=0)
    condition = models.BooleanField(default=True)

    def __str__ (self):
        """ Return Name Day """

        return self.name_day
        

class Sale(models.Model):
    
    CHOICES_METHOD_PAYMENT = [
        ('Cash','Cash'), 
        ('Card','Card')
        ]

    bookingspa = models.OneToOneField(BookingSpa, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=25, choices= CHOICES_METHOD_PAYMENT, default='Cash')
    price = models.FloatField()
    assistant = models.CharField(max_length=25, default='System')

    def __str__(self):

        return 'Booking N° {}'.format(self.bookingspa)

    
class Expenses(models.Model):

    distributor = models.ForeignKey(Distributor, on_delete=models.PROTECT)
    number = models.CharField(max_length=25, default='None')
    price_total = models.FloatField()
    description = models.CharField(max_length=250)
    classsification = models.CharField(
        max_length=25, choices=[
            ('cost','cost'),
            ('expense','expense')
        ], 
        default='expense')
    created = models.DateField()

    def __str__(self):
        return str(self.distributor)


class EmployeeHistoryBooking(models.Model):

    created = models.DateField()
    profile = models.ForeignKey(ProfileUser, on_delete=models.PROTECT)
    count_booking = models.IntegerField()
    count_service = models.IntegerField()
    commission_limit = models.IntegerField()

    def __str__(self):
        return '{} {}'.format(self.profile, self.created)


class ServiceEmployeeBooking(models.Model):

    employee = models.ForeignKey(EmployeeHistoryBooking, on_delete=models.PROTECT)
    name_service = models.CharField(max_length=25)
    price = models.FloatField()
    commission_percentage = models.FloatField()
    total_commission =  models.FloatField()
    created = models.DateTimeField()
    id_booking = models.IntegerField()

    def __str__(self):
        return '{}-{}'.format(self.employee.pk,self.employee) 


class CompanyData(models.Model):
    """ Create model company """

    name_company = models.CharField(max_length=25)
    document = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=25)
    phone_number = PhoneNumberField(unique=True)
    city = models.CharField(max_length=25)
    country = models.CharField(max_length=25)

    def __str__(self):
        return self.name_company


