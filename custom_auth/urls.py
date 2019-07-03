from django.urls import path

from custom_auth.views import CustomLoginView, CustomLogoutView, RegistrationView

app_name = 'custom_auth'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),


]
