from django.urls import path

from company import views
from company.views import *

app_name = 'company'

urlpatterns = [
    path('dashb', CompanyDashboardBaseView.as_view(), name='company_dashboard'),
    path('dashboard', CompanyDashboardIndexView.as_view(), name='company_dashboard_index'),

    path('jobpost', JobPostView.as_view(), name='job_post'),
    path('companydetail', CompanyDetailView.as_view(), name='company_detail'),
    path('apply', AppliedListView.as_view(), name='apply'),
    path('jobpostlist', JobPostListView.as_view(), name='jobpost_list'),
    path('jobpost/<slug:slug>/update', JobDetailUpdateView.as_view(), name='job_post_update'),

    path('profile/<slug:slug>/update', CompanyUpdateView.as_view(), name='company_update'),
    path('jobpost/<slug:slug>/delete', JobPostDeleteView.as_view(), name='job_post_delete'),
    path('password_change', CompanyChangePasswordView.as_view(), name='password_change'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),

]
