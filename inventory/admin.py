# Django
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

#model
from inventory.models import *


class ItemCleaningRoomResource(resources.ModelResource):

    class Meta:
        model = ItemCleaningRoom


@admin.register(ItemCleaningRoom)
class ItemCleaningRoomAdmin(ImportExportModelAdmin):
    """ItemCleaningRoom admin."""

    resource_class = ItemCleaningRoomResource
    list_display = ('id', 'roomspa', 'article', 'amount',)
    search_fields = ('roomspa', )
    list_per_page = 15


class RoomSpaResource(resources.ModelResource):

    class Meta:
        model = RoomSpa    


@admin.register(RoomSpa)
class RoomSpaAdmin(ImportExportModelAdmin):
    """RoomSpa admin."""

    resource_class = RoomSpaResource
    list_display = ('id', 'name', 'stretcher', 'condition',)
    search_fields = ('name', )
    list_filter = (
        'condition',
        'positon',
    )
    list_per_page = 15


class OutCellarResource(resources.ModelResource):

    class Meta:
        model = OutCellar  


@admin.register(OutCellar)
class OutCellarAdmin(ImportExportModelAdmin):
    """OutCellar admin."""

    resource_class = OutCellarResource
    list_display = ('id', 'article', 'amount', 'date',)
    search_fields = ('article', )
    list_per_page = 15


class InCellarResource(resources.ModelResource):

    class Meta:
        model = InCellar  


@admin.register(InCellar)
class InCellarAdmin(ImportExportModelAdmin):
    """InCellar admin."""

    resource_class = InCellarResource
    list_display = ('id', 'article', 'amount', 'date',)
    search_fields = ('article', )
    list_per_page = 15


class CellarGlobalResource(resources.ModelResource):

    class Meta:
        model = CellarGlobal  


@admin.register(CellarGlobal)
class CellarGlobalAdmin(ImportExportModelAdmin):
    """CellarGlobal admin."""

    resource_class = CellarGlobalResource
    list_display = ('id', 'article', 'in_cellar_balance', 'difference', 'cellar',)
    search_fields = ('article', )
    list_per_page = 15


class DistributorResource(resources.ModelResource):

    class Meta:
        model = Distributor  


@admin.register(Distributor)
class DistributorAdmin(ImportExportModelAdmin):
    """Distributor admin."""

    resource_class = DistributorResource
    list_display = ('id', 'name_distributor', 'document', 'name_contact','email', 'address', 'phone_number')
    search_fields = ('name_distributor', 'email')
    list_per_page = 15


class ClassificatioSupplieResource(resources.ModelResource):

    class Meta:
        model = ClassificatioSupplie  


@admin.register(ClassificatioSupplie)
class ClassificatioSupplieAdmin(ImportExportModelAdmin):
    """ClassificatioSupplie admin."""

    resource_class = ClassificatioSupplieResource
    list_display = ('id', 'name_area')
    search_fields = ('name_area',) 
    list_per_page = 15   


class SupplieResource(resources.ModelResource):

    class Meta:
        model = Supplie  


@admin.register(Supplie)
class SupplieAdmin(ImportExportModelAdmin):
    """Supplie admin."""

    resource_class = SupplieResource
    list_display = ('id', 'article','amount', 'price', 'distributor')
    search_fields = ('article',) 
    list_per_page = 15   
