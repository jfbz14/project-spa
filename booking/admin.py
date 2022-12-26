# Django
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Register your models here.
from .models import BookingSpa, ServiceAditional


class ServiceAditionalResource(resources.ModelResource):

    class Meta:
        model = ServiceAditional


@admin.register(ServiceAditional)
class ServiceAditionalAdmin(ImportExportModelAdmin):
    """ServiceAditional admin."""

    resource_class = ServiceAditionalResource
    list_display = ('pk', 'bookingspa', 'time_minutes', 'price', 'position', 'commission_percentage', 'created',  'modified')
    list_display_links = ('pk',)

    search_fields = (
        'bookingspa',
        'bookingspa__profile',
        'pk',
    )

    list_filter = (
        'position',
    )
    list_per_page = 15


class BookingSpaResource(resources.ModelResource):

    class Meta:
        model = BookingSpa


@admin.register(BookingSpa)
class BookingSpaAdmin(ImportExportModelAdmin):
    """BookingSpa admin."""

    resource_class = BookingSpaResource
    list_display = ('pk', 'client', 'profile', 'room', 'position', 'created', 'condition_pay', 'total_price')
    list_display_links = ('pk',)

    search_fields = (
        'client',
        'profile',
        'pk',
    )

    list_filter = (
        'position',
        'condition_pay',
        'created',
    )
    list_per_page = 15