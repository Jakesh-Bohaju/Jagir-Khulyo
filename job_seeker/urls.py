from django.urls import path

from job_seeker.views import *

app_name = 'job_seeker'

urlpatterns = [
    path('job_list', JobListView.as_view(), name='job_list'),
    path('category', CategoryListView.as_view(), name='category_list'),
    path('', SeekerDetailView.as_view(), name='seeker_detail')
]
