from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class ContactUsView(TemplateView):
    template_name = 'contact_us.html'
