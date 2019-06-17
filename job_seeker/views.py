from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView, CreateView

from job_seeker.forms import ResumeForm
from job_seeker.models import SeekerDetail
from home.models import Gender, Education


class JobListView(TemplateView):
    template_name = 'job_list.html'


class CategoryListView(TemplateView):
    template_name = 'job_category.html'


class FileForm(object):
    pass


class SeekerDetailView(CreateView):
    template_name = 'seeker_detail.html'
    model = SeekerDetail
    # fields = ['name', 'address', 'date_of_birth', 'phone_no','resume']
    form_class = ResumeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genders'] = Gender.objects.all()
        context['education'] = Education.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # form = self.get_form()
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            seeker_detail = form.save(commit=False)
            seeker_detail.user = request.user
            gender = request.POST.get('gend')
            education = request.POST.get('educ')
            gen = Gender.objects.get(gender=gender)
            edu = Education.objects.get(education=education)
            seeker_detail.gender_id = gen.id
            seeker_detail.education_id = edu.id
            seeker_detail.save()

            return redirect('job_seeker:job_list')

        else:
            print(form.errors)

        return redirect('job_seeker:seeker_detail')
