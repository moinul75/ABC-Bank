from django.urls import path

from .views import UserRegistrationView, LogoutView, UserLoginView,CustomPasswordChangeView,CustomPasswordChangeDoneView

app_name = 'accounts'

urlpatterns = [
    path("login/", UserLoginView.as_view(),name="user_login"),
    path("logout/", LogoutView.as_view(),name="user_logout"),
    path("register/", UserRegistrationView.as_view(),name="user_registration"),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
]