# Django
from django.urls import path

# View
from . import views


app_name = 'profileclient'

urlpatterns = [

    path(
        route='signup_client/',
        view=views.CreateProfileClient.as_view(),
        name='signup_client'
    ),
    path(
        route='list/clients/',
        view=views.ListViewClient.as_view(),
        name='list_client'
    ),
    path(
        route='update/client/<int:id>/',
        view=views.UpdateProfileClient.as_view(),
        name='update_client'
    ),
    path(
        route='update/history/client/<int:id>/',
        view=views.ListHistoryClient.as_view(),
        name='update_client_history'
    ),
]