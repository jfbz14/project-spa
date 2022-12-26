# Django
from django.urls import path

# View
from . import views


app_name = 'inventory'

urlpatterns = [

    # Distributor
    path(
        route='create/distributor/',
        view=views.CreateDistributor.as_view(),
        name='create_distributor'
    ),
    path(
        route='list/distributor',
        view=views.ListViewDistributor.as_view(),
        name='list_distributor'
    ),
    path(
        route='update/distributor/<int:id>/',
        view=views.UpdateDistributor.as_view(),
        name='update_distributor'
    ),

    # Classificationsupplie
    path(
        route='list/classificationsupplie/',
        view=views.ListViewClassificationSupplie.as_view(),
        name='list_classificationsupplie'
    ),
    
    path(
        route='create/classificationsupplie/',
        view=views.CreateClassificationSupplie.as_view(),
        name='create_classificationsupplie'
    ),

    # Supplie
    path(
        route='list/supplie/',
        view=views.ListViewSupplie.as_view(),
        name='list_supplie'
    ),
    path(
        route='create/supplie/',
        view=views.CreateSupplie.as_view(),
        name='create_supplie'
    ),
    path(
        route='update/supplie/<int:id>/',
        view=views.UpdateSupplie.as_view(),
        name='update_supplie'
    ),

    # Cellar
    path(
        route='list/cellar/',
        view=views.ListViewCellarGlobal.as_view(),
        name='list_cellar_global'
    ),

    # Incellar
    path(
        route='create/in_cellar/<int:id>/',
        view=views.CreateInCellar.as_view(),
        name='create_in_cellar'
    ),
    path(
        route='list/in_cellar/<int:id>/',
        view=views.ListViewInCellar.as_view(),
        name='list_in_cellar'
    ),

    # Outcellar
    path(
        route='create/out_cellar/<int:id>/',
        view=views.CreateOutCellar.as_view(),
        name='create_out_cellar'
    ),
    path(
        route='list/out_cellar/<int:id>/',
        view=views.ListViewOutCellar.as_view(),
        name='list_out_cellar'
    ),

    # Room
    path(
        route='list/room/',
        view=views.ListViewRoomSpa.as_view(),
        name='list_roomspa'
    ),
    path(
        route='update/room/<int:id>/',
        view=views.UpdateRoomSpa.as_view(),
        name='update_roomspa'
    ),
    path(
        route='create/room/',
        view=views.CreatedRoomSpa.as_view(),
        name='create_roomspa'
    ),

    # Item room
    path(
        route='list/itemroom/<int:id>/',
        view=views.ListViewItemCleaningRoom.as_view(),
        name='list_item_roomspa'
    ),
    path(
        route='create/itemroom/<int:id>/',
        view=views.CreateItemCleaningRoom.as_view(),
        name='create_item_roomspa'
    ),
    path(
        route='delete/itemroom/<int:id>/',
        view=views.DeleteItemCleaningRoom.as_view(),
        name='delete_item_roomspa'
    ),
]