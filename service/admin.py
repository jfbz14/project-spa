# Django
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

#model
from .models import Service, ItemService

class ItemServiceResource(resources.ModelResource):

    class Meta:
        model = ItemService 


@admin.register(ItemService)
class ItemServiceAdmin(ImportExportModelAdmin):
    """ItemService admin."""

    resource_class = ItemServiceResource
    list_display = ('pk', 'service', 'article', 'amount', 'price_amount',)
    list_display_links = ('pk',)
    search_fields = ('service', )
    list_per_page = 15


class ServiceResource(resources.ModelResource):

    class Meta:
        model = Service 

@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    """Service admin."""

    resource_class = ServiceResource
    list_display = ('pk', 'name', 'time_minutes', 'commission_percentage', 'price', 'created',)
    list_display_links = ('pk',)
    search_fields = ('name',)
    list_per_page = 15