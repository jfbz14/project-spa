# Django
from django.urls import path

# View
from profile_user import views


app_name = 'profileuser'

urlpatterns = [

    path(
        route='signup/user/',
        view=views.SignupView.as_view(),
        name='signup'
    ),
    path(
        route='',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='update/user/<int:id>/',
        view=views.UpdateProfileView.as_view(),
        name='update_profile'
    ),
    path(
        route='list/user/',
        view=views.ListViewProfile.as_view(),
        name='list_profile'
    ),
    path(
        route='change_password/user/',
        view=views.UserPasswordChangeView.as_view(),
        name='change_password'
    ),
    path(
        route='logout/user/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
]