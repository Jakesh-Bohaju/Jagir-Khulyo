from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class JobListView(TemplateView):
    template_name = 'job_list.html'


class CategoryListView(TemplateView):
    template_name = 'job_category.html'
