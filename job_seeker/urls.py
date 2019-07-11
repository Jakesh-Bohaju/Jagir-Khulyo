from django.urls import path

from job_seeker.views import *

app_name = 'job_seeker'

urlpatterns = [
    path('sdashb', SeekerDashboardBaseView.as_view(), name='seeker_dashboard'),
    path('sdashboard', SeekerDashboardIndexView.as_view(), name='seeker_dashboard_index'),
    path('job_list', JobListView.as_view(), name='job_list'),
    path('category', CategoryListView.as_view(), name='category_list'),
    path('', SeekerDetailView.as_view(), name='seeker_detail'),
    path('job_applied', SeekerAppliedView.as_view(), name='job_applied_list'),
    path('<slug:slug>/', JobDetailView.as_view(), name='single_job_detail'),
    path('profile/<slug:slug>/update', SeekerUpdateView.as_view(), name='seeker_update'),

]
