# Django
from django.urls import path

#model
from .views import *
# View

app_name = 'booking'

urlpatterns = [

   #Booking
   path(
      route='gestion/',
      view=ListViewBookingSpaGestion.as_view(),
      name='list_booking_gestion'
   ),
   path(
      route='list/wait/gestion/',
      view=ListViewBookingSpaWaitGestion.as_view(),
      name='list_booking_wait_gestion'
   ),
   path(
      route='list/active/gestion/',
      view=ListViewBookingSpaActiveGestion.as_view(),
      name='list_booking_active_gestion'
   ),

   path(
      route='create/booking/',
      view=CreateBooking.as_view(),
      name='create_bookingstart'
   ),
   path(
      route='create/booking/next/<int:id>/',
      view=CreateBookingNext.as_view(),
      name='create_bookingstarnext'
   ),
   path(
      route='cancel/booking/<int:id>/',
      view=CancelBookindSpa.as_view(),
      name='cancel_booking'
   ),
   path(
      route='create/service/aditional/<int:id>/',
      view=CreateServiceAditionalBooking.as_view(),
      name='create_serviceaditional_gte'
   ),
   path(
      route='cancel/service/aditional/<int:id>/',
      view=CancelServiceAditionalBookingSpa.as_view(),
      name='cancel_serviceaditional_gte'
   ),
   path(
      route='service/active/<int:id_employee>/<int:id_booking>/',
      view=UpdateBookingPositionActive.as_view(),
      name='active_booking'
   ),
   path(
      route='service/start/active/view/<int:id>/',
      view=DetailBookingActivate.as_view(),
      name='detail_bookingactivate'
   ),
   path(
      route='add/service/aditional/<int:id>/',
      view=AddServiceAditionalBookingActive.as_view(),
      name='add_serviceaditional_gte'
   ),
   path(
      route='end/service/booking/<int:id>/',
      view=FinalizedBookindSpa.as_view(),
      name='finalized_booking'
   ),
   path(
      route='list/wait/all/',
      view=ListBookingSpaWait.as_view(),
      name='list_booking_wait_all'
   ),
   path(
      route='pay/create/sale/booking/<int:id>/',
      view=CreateSaleBooking.as_view(),
      name='create_sale_booking'
   ),
   path(
      route='update/datetime/booking/<int:id>/',
      view=UpdateViewDateTimeBooking.as_view(),
      name='update_datetime_booking'
   ),
]