from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class JobPostView(TemplateView):
    template_name = 'jobpost.html'