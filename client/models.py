from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ProfileClient(models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ('CC', 'CEDULA DE CIUDADANIA'),
        ('CE', 'CEDULA DE EXTRANJERIA'),
        ('PA', 'PASAPORTE'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('IT', 'IDENTIFICACION TRIBUTARIA'),
        ('IP', 'IDENTIFICACION PERSONAL'),
    ]  

    SEX_TYPE_CHOICES = [
        ('F','FEMALE'),
        ('M','MALE'),
        ('UN','UNKNOWN'),
    ]

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    document_type = models.CharField(max_length=3, choices=DOCUMENT_TYPE_CHOICES)
    document_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    sex = models.CharField(max_length=2, choices=SEX_TYPE_CHOICES, default='UNKNOWN')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """ returun firts_name and last_name """

        if self.first_name == '':
            full_name = 'unknown'
        else:    
            full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class MedicalHistory(models.Model):

    client = models.OneToOneField(ProfileClient, on_delete=models.CASCADE)
    allergies = models.CharField(max_length=50, default='unknown')
    herpes = models.CharField(max_length=50, default='unknown')
    Skin_illness = models.CharField(max_length=50, default='unknown')
    condition = models.CharField(max_length=50, default='unknown')
    cardiac = models.CharField(max_length=50, default='unknown')
    hypertension = models.CharField(max_length=50, default='unknown')
    diabetes = models.CharField(max_length=50, default='unknown')
    thyroid = models.CharField(max_length=50, default='unknown')
    autoimmune_disease = models.CharField(max_length=50, default='unknown')
    surgical_history = models.CharField(max_length=50, default='unknown')
    pregnancy = models.CharField(max_length=50, default='unknown')
    ication = models.CharField(max_length=50, default='unknown')
    pacemaker = models.CharField(max_length=50, default='unknown')
    prosthesis = models.CharField(max_length=50, default='unknown')
    diu = models.CharField(max_length=50, default='unknown')
    implants = models.CharField(max_length=50, default='unknown')
    others = models.CharField(max_length=50, default='unknown')

    def __str__(self) -> str:
        """ returun firts_name and last_name """

        return str(self.client)
