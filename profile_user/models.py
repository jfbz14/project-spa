from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField

class User (AbstractUser):
    email = models.EmailField(blank=True, unique=True)



class ProfileUser (models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ('CC', 'CEDULA DE CIUDADANIA'),
        ('CE', 'CEDULA DE EXTRANJERIA'),
        ('PA', 'PASAPORTE'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('IT', 'IDENTIFICACION TRIBUTARIA'),
        ('IP', 'IDENTIFICACION PERSONAL'),
    ]  
    
    CONDITION_CHOICES = [
        ('disabled', 'disabled'),
        ('activated', 'activated'),
        ('occupied', 'occupied'),
    ]  

    CONDITION_BIOSAFETY_CHOICES = [
        ('disabled', 'disabled'),
        ('activated', 'activated'),
    ]  

    TYPE_CHARGE_CHOICES = [
        ('administrator', 'administrator'),
        ('assistant', 'assistant'),
        ('masseur', 'masseur'),
    ]

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    document_number = models.CharField(max_length=50, unique=True)
    picture = models.ImageField(upload_to='user/picture', blank=True, null=True,)
    phone_number = PhoneNumberField(unique=True)
    address = models.CharField(max_length=50, blank=True)
    academy = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=25, choices=TYPE_CHARGE_CHOICES, default='masseur')
    expiration_date_biosafety = models.DateField()
    condition_biosafety = models.CharField(max_length=15, choices=CONDITION_BIOSAFETY_CHOICES, null=True, blank=True)
    condition = models.CharField(max_length=25, choices=CONDITION_CHOICES, default='activated')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """ return firts_name and last_name """

        return self.user.get_full_name()

    def save(self, *args, **kwargs ):
        """validate biosafety certificate status, if expired, condition is false"""

        date_today = datetime.now().date()
        if self.expiration_date_biosafety < date_today:
            self.condition_biosafety = 'disabled'
        else:    
            self.condition_biosafety = 'activated'

        super().save(*args, **kwargs)      
