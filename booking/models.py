#django
from django.db import models
from datetime import timedelta

#model
from profile_user.models import ProfileUser
from client.models import ProfileClient
from inventory.models import RoomSpa


class BookingSpa(models.Model):
    """Model Bookinspa"""
        
    CHOICES_POSITION = [
        ('Active', 'Active'), 
        ('Cancel', 'Cancel'), 
        ('Finalized', 'Finalized'), 
        ('Wait', 'Wait')
        ]

    
    client = models.ForeignKey(ProfileClient, on_delete=models.PROTECT)
    profile = models.ForeignKey(ProfileUser, on_delete=models.PROTECT, blank=True, null=True)
    room = models.ForeignKey(RoomSpa, on_delete=models.PROTECT, blank=True, null=True)
    discount = models.IntegerField(default=0)
    advance_price = models.FloatField(default=0)
    balance = models.FloatField(blank=True, null=True, default=0)
    position = models.CharField(max_length=25, choices=CHOICES_POSITION, default='Wait')
    description = models.CharField(blank=True, null=True, default='None',max_length=50, help_text='Enter the reason, \n Minimum 10 characters. \n Maximum 50 characters.')
    created = models.DateTimeField()
    time_service = models.FloatField(default=0)
    end_hour = models.DateTimeField(blank=True, null=True)
    active = models.DateTimeField(blank=True, null=True)
    end_booking = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(blank=True, null=True, default=0)
    condition_pay = models.BooleanField(default=False) 

    def __str__(self):

        return '{}'.format(self.pk)  

 
class ServiceAditional(models.Model):

    CHOICES_POSITION = [
        ('Active','Active'),
        ('Cancel','Cancel')
    ]

    bookingspa = models.ForeignKey(BookingSpa, on_delete=models.PROTECT)  
    name_service = models.CharField(max_length=50)
    time_minutes = models.IntegerField()
    price = models.FloatField()
    commission_percentage = models.FloatField()
    position = models.CharField(max_length=6, choices=CHOICES_POSITION, default='Active')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):

        return '{} {}'.format(self.bookingspa.id, self.name_service)