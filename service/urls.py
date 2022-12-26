# Django
from django.urls import path

# View
from . import views

app_name = 'service'

urlpatterns = [
    
    path(
        route='create/service/',
        view=views.CreateService.as_view(),
        name='create_service'
    ),
    path(
        route='list/service/',
        view=views.ListViewService.as_view(),
        name='list_service'
    ),
    path(
        route='update/service/<int:id>/',
        view=views.UpdateService.as_view(),
        name='update_service'
    ),
    # Itemservice
    path(
        route='list/itemservice/<int:id>/',
        view=views.ListViewItemService.as_view(),
        name='list_itemservice'
    ),
    path(
        route='create/itemservice/<int:id>/',
        view=views.CreateItemService.as_view(),
        name='create_itemservice'
    ),
    path(
        route='delete/itemservice/<int:id>/',
        view=views.DeleteItemService.as_view(),
        name='delete_itemservice'
    ),
]