from django.urls import path
from company.views import *

app_names = 'company'

urlpatterns = [
    path('jobpost', JobPostView.as_view(), name='job_post')
]
