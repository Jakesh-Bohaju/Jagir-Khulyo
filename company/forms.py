from django import forms
from .models import *


class JobPostUpdateForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ('title', 'job_level', 'category', 'vacancy_no', 'experience', 'education', 'salary', 'description', 'deadline')
