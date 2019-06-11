from django.urls import path
from home.views import *

app_names = 'home'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
