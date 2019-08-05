from django import forms
from .models import *


# class JobPostUpdateForm(forms.ModelForm):
#     class Meta:
#         model = JobPost
#         fields = (
#             'title', 'job_level', 'category', 'vacancy_no', 'experience', 'education', 'salary', 'description',
#             'deadline')

# class CompanyDetailForm(forms.ModelForm):
#     class Meta:
#         model = CompanyDetail
#         fields = '__all__'

# def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.fields['district'].queryset = District.objects.none()
#
#     if 'province' in self.data:
#         try:
#             province_id = int(self.data.get('province_no'))
#             self.fields['district'].queryset = District.objects.filter(province_no_id=province_id).order_by('district')
#         except (ValueError, TypeError):
#             pass  # invalid input from the client; ignore and fallback to empty City queryset
#     elif self.instance.pk:
#         self.fields['district'].queryset = self.instance.province.district_set.order_by('district')
