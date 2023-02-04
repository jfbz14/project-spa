# Django
from django.urls import path

# Views
from . import views

app_name = 'administrator'

urlpatterns = [
    # Expense
    path(
        route='create/expense/',
        view=views.CreateExpense.as_view(),
        name='create_expense'
    ),
    path(
        route='list/expense/',
        view=views.ListViewExpenses.as_view(),
        name='list_expense'
    ),
    path(
        route='update/expense/<int:id>/',
        view=views.UpdateExpense.as_view(),
        name='update_expense'
    ),
    # Fixed Costs
    path(
        route='create/fixed_costs/',
        view=views.CreateFixedCosts.as_view(),
        name='create_fixed_costs'
    ),
    path(
        route='list/fixed_costs/',
        view=views.ListViewFixedCosts.as_view(),
        name='list_fixed_costs'
    ),
    path(
        route='update/fixed_costs/<int:id>/',
        view=views.UpdateFixedCosts.as_view(),
        name='update_fixed_costs'
    ),
    path(
        route='delete/fixed_costs/<int:id>/',
        view=views.DeleteFixedCosts.as_view(),
        name='delete_fixed_costs'
    ),
    # Admin Datetime Service
    path(
        route='list/day_datetime/',
        view=views.ListAdminDateTime.as_view(),
        name='list_admindatetime'
    ),
    path(
        route='update/day_datetime/<int:id>/',
        view=views.UpdateAdminDateTime.as_view(),
        name='update_admindatetime'
    ),
    # Booking
    path(
        route='list/booking/',
        view=views.ListViewBookingSpa.as_view(),
        name='list_booking'
    ),
    path(
        route='list/service/bookig/<int:id>/',
        view=views.ListServiceAditional.as_view(),
        name='list_service_booking'
    ),
    path(
        route='list/service/history/employee/',
        view=views.ListEmployeeServiceFinalized.as_view(),
        name='list_employee_service'
    ),
    path(
        route='update/service/history/employee/',
        view=views.UpdateEmployeeHistoryService.as_view(),
        name='update_employee_history_service'
    ),
    path(
      route='list/detail/service/history/employee/<int:id>/',
      view=views.ListServiceHistoryemployee.as_view(),
      name='list_detail_employee_history_service'
    ),
    path(
      route='list/sale/booking/',
      view=views.ListSaleBooking.as_view(),
      name='list_sale_booking'
    ),
    path(
      route='bookingspa/list/sale/true/',
      view=views.ListBookingSpaSaleTrue.as_view(),
      name='list_booking_sale_true'
    ),
    path(
      route='booking/file/<int:id>/',
      view= views.PdfView.as_view(),
      name='create_pdf_booking'
    ),
    path(
      route='dashboard/list/',
      view=views.ListDashBoard.as_view(),
      name='list_dashboard'
    ),
    
]

