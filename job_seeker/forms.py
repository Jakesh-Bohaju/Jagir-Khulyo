from django import forms
from .models import *


class ResumeForm(forms.ModelForm):
    class Meta:
        model = SeekerDetail
        fields = ['name', 'province', 'district', 'address', 'date_of_birth', 'phone_no', 'mobile_no', 'resume', 'image']
