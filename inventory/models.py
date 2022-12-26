# Django
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Distributor(models.Model):

    name_distributor = models.CharField(max_length=50, unique=True) 
    document  = models.CharField(max_length=50, unique=True)
    name_contact = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True, unique=True)
    address = models.CharField(max_length=50) 
    phone_number = PhoneNumberField(unique=True)

    def __str__(self):
        """ Return name distributor"""

        return self.name_distributor


class ClassificatioSupplie(models.Model):

    name_area = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """return name area"""

        return self.name_area


class Supplie(models.Model):

    UNIT_CHOICES = [
        ('und', 'und'),
        ('g', 'g'),
        ('ml', 'ml'),
    ]

    distributor = models.ForeignKey(Distributor, on_delete=models.PROTECT)
    classification = models.ForeignKey(ClassificatioSupplie, on_delete=models.PROTECT) 
    article = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES)
    amount = models.FloatField()
    price = models.FloatField()
    price_unit = models.FloatField(null=True, blank=True)

    def __str__(self):
        """return article"""

        return self.article

    def save(self, *args, **kwargs ):
        self.price_unit = self.price / self.amount
        super().save(*args, **kwargs)


class InCellar(models.Model):
    
    article = models.ForeignKey(Supplie, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    unit = models.CharField(max_length=50, null=True, blank=True)       
    description = models.CharField(max_length=50)

    def __str__(self):
        """return article and amount"""

        return '{} = {}'.format(self.article, self.amount)

    def save(self, *args, **kwargs):
        self.unit = self.article.unit
        super().save(*args, **kwargs)    

    
class OutCellar(models.Model):
    
    date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Supplie, on_delete=models.PROTECT)
    amount = models.FloatField()
    unit = models.CharField(max_length=50, null=True, blank=True)       
    description = models.CharField(max_length=50)

    def __str__(self):
        """return article and amount"""

        return '{} = {}'.format(self.article, self.amount)

    def save(self, *args, **kwargs):
        self.unit = self.article.unit
        super().save(*args, **kwargs)    


class CellarGlobal(models.Model):

    article = models.OneToOneField(Supplie, on_delete=models.PROTECT)
    in_cellar = models.FloatField(null=True, blank=True)
    out_cellar = models.FloatField(null=True, blank=True)
    in_cellar_balance = models.FloatField(default=0)
    difference = models.FloatField(null=True, blank=True)
    cellar = models.FloatField(null=True, blank=True) 
    unit = models.CharField(max_length=50, null=True, blank=True)       

    def __str__(self):
        """return article and cellar"""

        return '{} = {}'.format(self.article, self.cellar)

    def save(self, *args, **kwargs):
        self.unit = self.article.unit
        queryincellar = InCellar.objects.filter(article=self.article).exists()
        queryoutcellar = OutCellar.objects.filter(article=self.article).exists()

        if queryincellar:
            """ If the article exists, look for the model save its quantities. """
            in_cellar_query = InCellar.objects.filter(article=self.article).values('amount')
            incellar =float()
            for in_cellarglobal in in_cellar_query:
                incellar += float(in_cellarglobal['amount'])
            self.in_cellar = incellar
        else:
            self.in_cellar = 0.0    

        if queryoutcellar:
            """ If the article exists, look for the model save its quantities. """
            out_cellar_query = OutCellar.objects.filter(article=self.article).values('amount')
            outcellar =float()
            for out in out_cellar_query:
                outcellar += float(out['amount'])
            self.out_cellar = outcellar
        else:
            self.out_cellar = 0.0    

        self.cellar = self.in_cellar - self.out_cellar    
        self.difference = self.in_cellar_balance - self.cellar 

        super().save(*args, **kwargs)
           

class RoomSpa(models.Model):

    name = models.CharField(max_length=25, unique=True)
    stretcher = models.CharField(max_length=50)
    condition = models.BooleanField(default=True)
    positon = models.BooleanField(default=True)

    def __str__(self):
        """return name stretcher and condition"""

        return '{}'.format(self.name)

         
class ItemCleaningRoom(models.Model):

    roomspa = models.ForeignKey(RoomSpa, on_delete=models.PROTECT)   
    article = models.ForeignKey(Supplie, on_delete=models.PROTECT)
    amount = models.FloatField()  
    unit = models.CharField(max_length=25, null=True, blank=True)
    price_amount = models.FloatField(null=True, blank=True) 


    def __str__(self):
        """return roomspa and itemcelaning"""

        return '{} - {}'.format(self.roomspa, self.article)

    def save(self, *args, **kwargs):
        self.unit = self.article.unit
        self.price_amount = self.amount * self.article.price_unit
        super().save(args, **kwargs)     
