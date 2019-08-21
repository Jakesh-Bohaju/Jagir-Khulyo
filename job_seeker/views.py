from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from company.models import *
from job_seeker.forms import ResumeForm


class SeekerDashboardBaseView(TemplateView):
    template_name = '_job_seeker_dashboard_base_2.html'
    model = SeekerDetail
    success_url = reverse_lazy('job_seeker:seeker_dashboard_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class SeekerDashboardIndexView(TemplateView):
    template_name = 'job_seeker_dashboard.html'
    model = SeekerDetail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['user'] = SeekerDetail.objects.get(user_id=user)
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class SeekerDetailView(CreateView):
    template_name = 'seeker_detail.html'
    model = SeekerDetail
    # fields = ['name', 'province', 'district', 'address', 'date_of_birth', 'phone_no','resume','image']
    form_class = ResumeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genders'] = Gender.objects.all()
        context['education'] = Education.objects.all()
        user = self.request.user
        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
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


class SeekerUpdateView(UpdateView):
    model = SeekerDetail
    fields = ['name', 'province', 'district', 'address', 'date_of_birth', 'gender', 'phone_no', 'mobile_no',
              'education', 'resume', 'image']
    template_name = 'seeker_update_form.html'
    success_url = reverse_lazy('job_seeker:seeker_dashboard_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class SeekerAppliedView(ListView):
    model = ReceivedResume
    template_name = 'job_applied.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['applied_list'] = ReceivedResume.objects.filter(applicant_name__user=user)
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class ChangePasswordView(PasswordChangeView):
    template_name = 'password_change_form.html'
    success_url = reverse_lazy('job_seeker:seeker_dashboard_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


def load_districts(request):
    province_id = request.GET.get('province')
    districts = District.objects.filter(province_no_id=province_id).order_by('district')
    return render(request, 'dropdown_district.html', {'districts': districts})
