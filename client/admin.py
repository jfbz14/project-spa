# Django
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Model
from client.models import ProfileClient, MedicalHistory


class ProfileClientResource(resources.ModelResource):

    class Meta:
        model = ProfileClient


class MedicalHistoryResource(resources.ModelResource):

    class Meta:
        model = MedicalHistory


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(ImportExportModelAdmin):
    """MedicalHistory admin."""

    resource_class = MedicalHistoryResource
    list_display = ('pk','client', )
    list_display_links = ('pk',)

    search_fields = (
        'client',
    )
    list_per_page = 15


@admin.register(ProfileClient)
class ProfileAdmin(ImportExportModelAdmin):
    """client admin."""

    resource_class = ProfileClientResource
    list_display = ('pk','first_name', 'last_name', 'document_number', 'document_number')
    list_display_links = ('pk',)

    search_fields = (
        'first_name',
        'document_number',
        'last_name',
    )
    list_per_page = 15