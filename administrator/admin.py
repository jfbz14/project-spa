# Django
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Register your models here.
from .models import Expenses, AdminDateService, Sale, EmployeeHistoryBooking, ServiceEmployeeBooking, CompanyData


class CompanyDataResource(resources.ModelResource):

    class Meta:
        model = CompanyData

@admin.register(CompanyData)
class CompanyDataAdmin(ImportExportModelAdmin):
    """CompanyData admin."""

    resource_class = CompanyDataResource
    list_display = ('pk', 'name_company', 'document', 'email', 'address', 'phone_number', 'city', 'country',)
    list_display_links = ('pk',)

    search_fields = (
        'name_company',
    )
    list_per_page = 15


class ServiceEmployeeBookingResource(resources.ModelResource):

    class Meta:
        model = ServiceEmployeeBooking


@admin.register(ServiceEmployeeBooking)
class ServiceEmployeeBookingAdmin(ImportExportModelAdmin):
    """ServiceEmployeeBooking admin."""

    resource_class = ServiceEmployeeBookingResource
    list_display = ('pk', 'employee', 'name_service', 'id_booking', 'price', 'created',)
    list_display_links = ('pk',)

    search_fields = (
        'employee',
        'id_booking',
        'pk',
    )

    list_filter = (
        'created',
    )
    list_per_page = 15


class EmployeeHistoryBookingResource(resources.ModelResource):

    class Meta:
        model = EmployeeHistoryBooking


@admin.register(EmployeeHistoryBooking)
class EmployeeHistoryBookingAdmin(ImportExportModelAdmin):
    """EmployeeHistoryBooking admin."""

    resource_class = EmployeeHistoryBookingResource
    list_display = ('pk', 'profile', 'created',)
    list_display_links = ('pk',)

    search_fields = (
        'profile',
        'pk',
    )

    list_filter = (
        'created',
    )
    list_per_page = 15


class SaleResource(resources.ModelResource):

    class Meta:
        model = Sale


@admin.register(Sale)
class SaleAdmin(ImportExportModelAdmin):
    """Sale admin."""

    resource_class = SaleResource
    list_display = ('pk', 'bookingspa', 'price', 'created', 'payment_method',  'assistant')
    list_display_links = ('pk',)

    search_fields = (
        'bookingspa',
        'bookingspa__profile',
        'pk',
    )

    list_filter = (
        'payment_method',
    )
    list_per_page = 15


class AdminDateServiceResource(resources.ModelResource):

    class Meta:
        model = AdminDateService


@admin.register(AdminDateService)
class AdminDateServiceAdmin(ImportExportModelAdmin):
    """AdminDateService admin."""

    resource_class = AdminDateServiceResource
    list_display = ('pk', 'name_day', 'time_start', 'time_end', 'commission_limit', 'condition',)
    list_display_links = ('pk',)

    search_fields = (
        'name_day',
        'pk',
    )

    list_filter = (
        'condition',
    )
    list_per_page = 15


class ExpensesResource(resources.ModelResource):

    class Meta:
        model = Expenses


@admin.register(Expenses)
class ExpensesAdmin(ImportExportModelAdmin):
    """Expenses admin."""

    resource_class = ExpensesResource
    list_display = ('pk', 'distributor', 'number', 'price_total', 'classsification', 'created')
    list_display_links = ('pk',)

    search_fields = (
        'distributor',
        'number',
        'classsification',
    )

    list_filter = (
        'classsification',
        'created',
    )
    list_per_page = 15