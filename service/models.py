from django.db import models
from inventory.models import Supplie


class Service(models.Model):

    name = models.CharField(max_length=50, unique=True)
    time_minutes = models.IntegerField()
    commission_percentage = models.FloatField()
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return name service"""

        return self.name
  

class ItemService(models.Model):

    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    article = models.ForeignKey(Supplie, on_delete=models.PROTECT)
    unit = models.CharField(max_length=25, null=True, blank=True)
    amount = models.FloatField()
    price_amount = models.FloatField(null=True, blank=True) 

    def __str__(self):
        """return service and article"""

        return '{} {}'.format(self.service, self.article)

    def save(self, *args, **kwargs):
        self.unit = self.article.unit
        self.price_amount = self.amount * self.article.price_unit
        super().save(args, **kwargs)  