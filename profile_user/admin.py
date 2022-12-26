# Django
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Model
from .models import User, ProfileUser


admin.site.site_header = 'App Guiatec'
admin.site.index_title = 'App Guiatec'
admin.site.site_title = 'App Guiatec'


class ProfileUserResource(resources.ModelResource):

    class Meta:
        model = ProfileUser


class UserResource(resources.ModelResource):

    class Meta:
        model = User


@admin.register(User)
class UserProfileAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = UserResource
    list_per_page = 15


@admin.register(ProfileUser)
class ProfileUserAdmin(ImportExportModelAdmin):
    """Profile admin."""

    resource_class = ProfileUserResource
    list_display = ('pk', 'user', 'document_type', 'document_number', 'phone_number', 'position')
    list_display_links = ('pk', 'user',)

    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
        'document_number'
    )

    list_filter = (
        'user__is_active',
        'user__is_staff',
        'position',
        'created',
        'modified',
    )

    list_per_page = 15