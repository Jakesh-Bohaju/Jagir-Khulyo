from django.urls import path

from cms.views import *

app_name = 'cms'
urlpatterns = [

    path('about-us/', AboutUsView.as_view(), name="about_us"),
    path('contact-us/', ContactUsView.as_view(), name="contact_us"),

]
