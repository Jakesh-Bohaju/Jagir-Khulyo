from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import CreateView, UpdateView

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
            return redirect('home:index')

        return redirect('company:job_post')


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
    template_name = 'job_apply_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['apply_title'] = JobPost.objects.filter(company__user_id=user)
        context['apply_list'] = ReceivedResume.objects.filter(job_title__company__user_id=user)

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print("before form validate")

        if form.is_valid():
            print("after form validation")
            a = form.save(commit=False)
            b = request.user.id
            jobsek = SeekerDetail.objects.all()
            for i in jobsek:
                if i.user_id == b:
                    a.applicant_name_id = i.id

            a.save()

            return redirect('job_seeker:job_list')

        return redirect('job_seeker:job_list')


# class JobPostUpdateView(UpdateView):
#     template_name = 'jobpost.html'
#     model = JobPost
#     fields = ['title', 'job_level', 'vacancy_no', 'experience', 'salary', 'description', 'deadline']
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         context['education'] = Education.objects.all()
#         return context
#
#     # def post(self, request, *args, **kwargs):
#     #
#     #     form = self.get_form()
#     #     if form.is_valid():
#     #
#     #         job_post = form.save(commit=False)
#     #         category = request.POST.get('cate')
#     #         education = request.POST.get('ed')
#     #         cat = Category.objects.get(category=category)
#     #         edu = Education.objects.get(education=education)
#     #         job_post.category_id = cat.id
#     #         job_post.education_id = edu.id
#     #         user = request.user
#     #         company = CompanyDetail.objects.all()
#     #         for i in company:
#     #             if user.id == i.user_id:
#     #                 job_post.company_id = i.id
#     #         job_post.save()
#     #         return redirect('home:index')
#     #   return redirect('company:job_post')
#
#     def form_valid(self, form):
#         job_post = form.save(commit=False)
#         category = self.request.POST.get('cate')
#         education = self.request.POST.get('ed')
#         cat = Category.objects.get(category=category)
#         edu = Education.objects.get(education=education)
#         job_post.category_id = cat.id
#         job_post.education_id = edu.id
#         user = self.request.user
#         company = CompanyDetail.objects.all()
#         for i in company:
#             if user.id == i.user_id:
#                 job_post.company_id = i.id
#         self.job_post = form.save()
#         return super().form_valid(form)
