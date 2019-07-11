from django import forms
from .models import *


class ResumeForm(forms.ModelForm):
    class Meta:
        model = SeekerDetail
        fields = ['name', 'address', 'date_of_birth', 'phone_no', 'resume', 'image']
