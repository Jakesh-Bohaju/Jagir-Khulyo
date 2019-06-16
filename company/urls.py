from django.urls import path
from company.views import *

app_name = 'company'

urlpatterns = [
    path('jobpost', JobPostView.as_view(), name='job_post'),
    path('companydetail', CompanyDetailView.as_view(), name='company_detail')
]
