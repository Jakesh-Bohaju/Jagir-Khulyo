from django.urls import path
from home.views import *

app_name = 'home'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search', SearchView.as_view(), name='search_job'),
]
