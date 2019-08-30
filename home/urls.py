from django.urls import path
from home.views import *

app_name = 'home'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search', SearchView.as_view(), name='search_job'),
    path('job_list', JobListView.as_view(), name='job_list'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category_list'),
    path('job-detail/<slug:slug>/', JobDetailView.as_view(), name='single_job_detail'),
    path('pagenotfound', Error404.as_view(), name='error_page'),
    path('faq', FaqView.as_view(), name="faq"),
    path('job_by/<slug:slug>/', LocationListView.as_view(), name="jbl"),
    path('jobtype/<slug:slug>/', JobTypeView.as_view(), name="jbt"),

]
