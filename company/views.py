from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView, CreateView

from company.models import *
from home.models import Category, Education


class JobPostView(CreateView):
    template_name = 'jobpost.html'
    model = JobPost
    fields = ['title', 'job_level', 'vacancy_no', 'experience', 'salary', 'description', 'deadline']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['education'] = Education.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():

            job_post = form.save(commit=False)
            category = request.POST.get('cate')
            education = request.POST.get('ed')
            cat = Category.objects.get(category=category)
            edu = Education.objects.get(education=education)
            job_post.category_id = cat.id
            job_post.education_id = edu.id
            user = request.user
            company = CompanyDetail.objects.all()
            for i in company:
                if user.id == i.user_id:
                    job_post.company_id = i.id
            job_post.save()
            return redirect('company:job_post')

        return redirect('home:index')


class CompanyDetailView(CreateView):
    template_name = 'company_detail.html'
    model = CompanyDetail
    fields = ['company_name', 'address', 'company_type', 'phone_no']

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            detail = form.save(commit=False)
            detail.user = request.user
            detail.save()
            return redirect('company:job_post')
        return redirect('company:company_detail')


class AppliedListView(CreateView):
    model = ReceivedResume
    fields = ['job_title']
    template_name = 'apply_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_apply'] = ReceivedResume.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            a = form.save(commit=False)
            b = request.user.id
            jobsek = SeekerDetail.objects.all()
            for i in jobsek:
                if i.user_id == b:
                    a.applicant_name_id = i.id

            a.save()

            return redirect('/')

        return redirect('/custom/login')

