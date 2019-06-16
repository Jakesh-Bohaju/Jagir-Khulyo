from django.urls import path

from custom_auth.views import CustomLoginView, CustomLogoutView, RegisterView

app_name = 'custom_auth'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

]
