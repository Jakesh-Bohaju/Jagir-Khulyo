from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect, render
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView

from company.models import *
from home.models import Category, Education


# from company.forms import CompanyDetailForm


class CompanyDashboardBaseView(TemplateView):
    template_name = '_company_dashboard_base.html'
    model = CompanyDetail
    success_url = reverse_lazy('company:company_dashboard_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class CompanyDashboardIndexView(TemplateView):
    template_name = 'company_dashboard_index.html'
    model = CompanyDetail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            # context['user'] = CompanyDetail.objects.get(user_id=user)
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class JobPostView(LoginRequiredMixin, CreateView):
    template_name = 'jobpost.html'
    model = JobPost
    fields = ['title', 'vacancy_no', 'experience', 'salary', 'negotiable', 'description', 'job_requirement',
              'deadline']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        try:
            context['categories'] = Category.objects.all()
            context['education'] = Education.objects.all()
            context['job_levels'] = JobLevel.objects.all()
            context['job_types'] = JobType.objects.all()
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        print("before form validation")
        if form.is_valid():
            print("after form validation")
            job_post = form.save(commit=False)
            category = request.POST.get('cate')
            education = request.POST.get('ed')
            joblevel = request.POST.get('jl')
            jobtype = request.POST.get('jt')
            cat = Category.objects.get(category=category)
            edu = Education.objects.get(education=education)
            job_level = JobLevel.objects.get(job_level=joblevel)
            job_type = JobType.objects.get(job_type=jobtype)
            job_post.category_id = cat.id
            job_post.education_id = edu.id
            job_post.job_level_id = job_level.id
            job_post.job_type_id = job_type.id
            user = request.user
            company = CompanyDetail.objects.all()
            for i in company:
                if user.id == i.user_id:
                    job_post.company_id = i.id
            job_post.save()
            return redirect('home:index')

        else:
            print(form.errors)

        return redirect('company:job_post')


class CompanyDetailView(CreateView):
    template_name = 'company_detail.html'
    model = CompanyDetail
    # form_class = CompanyDetailForm
    fields = ['company_name', 'province', 'district', 'address', 'company_type', 'phone_no', 'mobile_no',
              'company_registration_date',
              'company_image']

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['provinces'] = Province.objects.all()
    #     context['districts'] = District.objects.all()

    # return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            detail = form.save(commit=False)
            detail.user = request.user
            # province = request.POST.get('province')
            # district = request.POST.get('district')
            # prov = Province.objects.get(province_name=province)
            # dis = District.objects.get(district=district)
            # detail.province_id = prov.id
            # detail.district_id = dis.id
            detail.save()
            return redirect('company:job_post')
        else:
            print(form.errors)

        return redirect('company:company_detail')


class AppliedListView(LoginRequiredMixin, CreateView):
    model = ReceivedResume
    fields = ['job_title', 'status', 'accepted']
    template_name = 'job_apply_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            context['apply_title'] = JobPost.objects.filter(company__user_id=user)
            context['apply_list'] = ReceivedResume.objects.filter(job_title__company__user_id=user)
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        applied_email = request.POST.get('ap_email')
        applied_name = request.POST.get('ap_name')
        subject = 'Hiring for Job'
        message = render_to_string('hiring_job.html', {
            'user': applied_name
        })
        msg = EmailMessage(subject, message, to=[applied_email])
        msg.send()

        if form.is_valid():
            a = form.save(commit=False)
            b = request.user.id
            jobsek = SeekerDetail.objects.all()
            for i in jobsek:
                if i.user_id == b:
                    a.applicant_name_id = i.id

            a.save()

            return redirect('home:job_list')

        return redirect('home:job_list')


class JobPostListView(LoginRequiredMixin, ListView):
    template_name = 'jobpost_list.html'
    model = JobPost
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id

        try:
            context['joblists'] = JobPost.objects.filter(company__user_id=user)
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class JobDetailUpdateView(UpdateView):
    model = JobPost
    fields = ['title', 'job_level', 'category', 'vacancy_no', 'experience', 'education', 'salary', 'negotiable',
              'job_type', 'description', 'job_requirement',
              'deadline']
    template_name = 'jobpost_update_form.html'
    success_url = reverse_lazy('company:jobpost_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class CompanyUpdateView(UpdateView):
    model = CompanyDetail
    fields = ['company_name', 'province', 'district', 'address', 'company_type', 'phone_no', 'mobile_no',
              'company_registration_date',
              'company_image']
    template_name = 'company_update_form.html'
    success_url = reverse_lazy('company:company_dashboard_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class JobPostDeleteView(DeleteView):
    model = JobPost
    success_url = reverse_lazy('company:job_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class CompanyChangePasswordView(PasswordChangeView):
    template_name = 'company_password_change_form.html'
    success_url = reverse_lazy('company:company_dashboard_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


def load_districts(request):
    province_id = request.GET.get('province')
    districts = District.objects.filter(province_no_id=province_id).order_by('district')
    return render(request, 'dropdown_district.html', {'districts': districts})


class JobAppliedNotificationView(CreateView):
    template_name = 'notification.html'
    model = ReceivedResume
    fields = ['status']
    success_url = reverse_lazy('company:notification_job_update')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            context['apply_title'] = JobPost.objects.filter(company__user_id=user)
            context['apply_list'] = ReceivedResume.objects.filter(job_title__company__user_id=user)
            context['menu_option'] = CompanyDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context

    def post(self, request, *args, **kwargs):
        b = request.user.id
        applied = ReceivedResume.objects.filter(job_title__company__user_id=b)
        jtid = int(request.POST.get('jt'))
        for i in applied:

            if i.job_title_id == jtid:
                i.status = True
                i.save()

        return redirect('company:notification_job')
