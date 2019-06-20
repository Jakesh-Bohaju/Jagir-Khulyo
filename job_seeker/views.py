from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView, CreateView, ListView, DetailView

from job_seeker.forms import ResumeForm
from job_seeker.models import SeekerDetail
from home.models import Gender, Education
from company.models import *


class JobListView(ListView):
    template_name = 'job_list.html'
    model = JobPost
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['jobs'] = JobPost.objects.all()
        context['categories'] = Category.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['latest_jobs'] = JobPost.objects.all().order_by('-id')
        context['freq_categories'] = Category.objects.all().order_by('?')
        return context


class CategoryListView(ListView):
    template_name = 'job_category.html'
    model = Category
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.all()
        context['freq_categories'] = Category.objects.all().order_by('?')
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        return context


class JobDetailView(DetailView):
    model = JobPost
    template_name = 'single_job.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['job'] = JobPost.objects.get(slug=slug)
        return context


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
