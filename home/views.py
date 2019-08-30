import datetime

from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import date
from django.views.generic import TemplateView, ListView, DetailView

from blog.models import Blog
from company.models import JobPost, Category, CompanyDetail, Faq, IPTracker, ReceivedResume
from home.models import JobType, District
from job_seeker.models import SeekerDetail


class IndexView(ListView):
    template_name = 'index.html'
    model = JobPost
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['jobsss'] = JobPost.objects.all()
        context['jobtype'] = JobType.objects.all()
        context['categories'] = Category.objects.all().order_by('?')
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['latest_jobs'] = JobPost.objects.all().order_by('-id')
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['companies'] = CompanyDetail.objects.all()
        context['alljobcount'] = self.object_list.all().count()
        aa = self.object_list.all()
        today = datetime.datetime.now()
        obj_list = []
        for i in aa:
            if i.deadline.year >= today.year and i.deadline.month >= today.month and i.deadline.day >= today.day:
                self.object_list = i
                obj_list.append(self.object_list)

        # context['object_list'] = obj_list
        for i in obj_list:
            print(i)

        sss = District.objects.annotate(Count('company_detail_district__job_post_company')).order_by(
            '-company_detail_district__job_post_company__count')[:5]
        afd = []
        for i in sss:
            a = str(JobPost.objects.filter(company__district__district=i).count())
            aa = {'district': i.district, 'count': a}
            afd.append(aa)
        context['jbl'] = afd

        return context

    def post(self, request, *args, **kwargs):
        x = request.POST.get('job')
        a = JobPost.objects.get(id=x)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_data1 = x_forwarded_for.split(',')[0]
        else:
            ip_data1 = request.META.get('REMOTE_ADDR')

        aa = timezone.now()
        now = timezone.now() - timezone.timedelta(hours=24)
        asd = IPTracker()
        obj = IPTracker.objects.filter(job_ip_id=x)
        temp = 0

        # try to save user ip with respect to ip address only
        # try:
        #     if obj.exists():
        #         for i in obj:
        #             if i.ip_data == ip_data1:
        #                 temp = 0
        #                 break
        #             else:
        #                 temp = 1
        #         if temp == 1:
        #             asd.ip_data = ip_data1
        #             asd.job_ip_id = request.POST.get('job')
        #             asd.user_ip_id = request.POST.get('user')
        #             asd.save()
        #
        #     else:
        #         asd.ip_data = ip_data1
        #         asd.job_ip_id = request.POST.get('job')
        #         asd.user_ip_id = request.POST.get('user')
        #         asd.save()
        # except Exception as e:
        #     print(e)

        # try to save user ip with respect to ip address and view the job 24 hours ago
        try:
            if obj.exists():
                for i in obj:
                    if i.date_time > now and i.ip_data == ip_data1:
                        temp = 0
                        break
                    else:
                        temp = 1

                if temp == 1:
                    asd.ip_data = ip_data1
                    asd.job_ip_id = request.POST.get('job')
                    asd.user_ip_id = request.POST.get('user')
                    asd.save()
            else:
                asd.ip_data = ip_data1
                asd.job_ip_id = request.POST.get('job')
                asd.user_ip_id = request.POST.get('user')
                asd.save()

        except Exception as e:
            print(e)

        return redirect('/job-detail/' + a.slug)


class SearchView(ListView):
    template_name = 'search_result.html'
    model = JobPost
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title')
        location = request.GET.get('location')
        category = request.GET.get('category')
        search_set = JobPost.objects.filter()
        # b = []
        if request.GET.get('title') and request.GET.get('location') and request.GET.get('category'):
            search_set = search_set.filter(title__icontains=title, company__district__district__icontains=location,
                                           category__category__icontains=category)

        elif request.GET.get('title') and request.GET.get('location') or request.GET.get('category'):
            search_set = search_set.filter(title__icontains=title, company__district__district__icontains=location,
                                           category__category__icontains=category)

        elif request.GET.get('title') or request.GET.get('location') and request.GET.get('category'):
            search_set = search_set.filter(title__icontains=title, company__district__district__icontains=location,
                                           category__category__icontains=category)
        elif request.GET.get('title') or request.GET.get('location') or request.GET.get('category'):
            search_set = search_set.filter(title__icontains=title, company__district__district__icontains=location,
                                           category__category__icontains=category)

        # print(b)
        template_context = {
            'filtered_jobs': search_set,
            'top_jobs': JobPost.objects.all().order_by('?'),
            'latest_jobs': JobPost.objects.all().order_by('-id')[:6],
            'freq_categories': Category.objects.all().order_by('?'),
            'blogs': Blog.objects.all().order_by('?')[:3],
            'job_by_locations': JobPost.objects.all(),
            'jobtype': JobType.objects.all(),
        }
        return render(request, 'search_result.html', template_context)


class Error404(TemplateView):
    template_name = 'error_404.html'


class JobListView(ListView):
    template_name = 'job_list.html'
    model = JobPost
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['jobs'] = JobPost.objects.all()
        context['jobtype'] = JobType.objects.all()
        context['freq_categories'] = Category.objects.all().order_by('?')
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['latest_jobs'] = JobPost.objects.all().order_by('-id')
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['companies'] = CompanyDetail.objects.all()
        user = self.request.user
        today = datetime.datetime.now()
        aa = self.object_list.all()
        obj_list = []
        for i in aa:
            if i.deadline.year >= today.year and i.deadline.month >= today.month and i.deadline.day >= today.day:
                self.object_list = i
                obj_list.append(self.object_list)

        # context['object_list'] = obj_list
        sss = District.objects.annotate(Count('company_detail_district__job_post_company')).order_by(
            '-company_detail_district__job_post_company__count')[:5]
        afd = []
        for i in sss:
            a = str(JobPost.objects.filter(company__district__district=i).count())
            aa = {'district': i.district, 'count': a}
            afd.append(aa)
        context['jbl'] = afd

        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)

        return context


class CategoryListView(ListView):
    template_name = 'job_list.html'
    model = JobPost
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.all()
        user = self.request.user
        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        context['freq_categories'] = Category.objects.all().order_by('?')
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['jobtype'] = JobType.objects.all()

        category = self.kwargs.get('slug')
        queryset = self.model.objects.filter(category__slug=category)
        context['object_list'] = queryset
        for i in queryset:
            print(i)

        sss = District.objects.annotate(Count('company_detail_district__job_post_company')).order_by(
            '-company_detail_district__job_post_company__count')[:5]
        afd = []
        for i in sss:
            a = str(JobPost.objects.filter(company__district__district=i).count())
            aa = {'district': i.district, 'count': a}
            afd.append(aa)
        context['jbl'] = afd
        return context


class JobDetailView(DetailView):
    model = JobPost
    template_name = 'single_job.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        job = JobPost.objects.get(slug=slug)
        context['counts'] = IPTracker.objects.filter(job_ip__slug=slug).count()
        abc = ReceivedResume.objects.filter(job_title__slug=slug).count()
        uvw = abc + 1
        xyz = int(str(abc)[-1])
        today = date.today()
        dayss = job.deadline - today
        weeks = int(dayss.days / 7)
        days = dayss.days % 7
        context['dayssss'] = dayss.days
        context['week'] = weeks
        context['days'] = days
        context['applicant'] = uvw
        context['applicantsplit'] = xyz
        context['job'] = job
        context['alljob'] = JobPost.objects.all()
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['company'] = CompanyDetail.objects.get(job_post_company=job)
        asd = ReceivedResume.objects.all()
        user = self.request.user
        context['already_applied'] = ReceivedResume.objects.filter(job_title__slug=slug,
                                                                   applicant_name__user_id=user.id).exists()
        sss = District.objects.annotate(Count('company_detail_district__job_post_company')).order_by(
            '-company_detail_district__job_post_company__count')[:5]
        afd = []
        for i in sss:
            a = str(JobPost.objects.filter(company__district__district=i).count())
            aa = {'district': i.district, 'count': a}
            afd.append(aa)
        context['jbl'] = afd

        count = 0
        popost = []
        for i in JobPost.objects.all():
            for j in IPTracker.objects.all():
                if i.id == j.job_ip_id:
                    count = count + 1
            # print('Job: ', i.title, '\ni.id:', i.id, '\ncount: ', count)
            popost.append({'job': i.title, 'jid': i.id, 'count': count})
            count = 0
        context['popular_job'] = sorted(popost, key=lambda x: (x['count'], x['jid']), reverse=True)[:10]

        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        return context


class FaqView(TemplateView):
    template_name = 'faq.html'
    model = Faq

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sfaqs'] = Faq.objects.filter(role='job_seeker')
        context['cfaqs'] = Faq.objects.filter(role='company')

        return context


class LocationListView(ListView):
    model = JobPost
    template_name = 'job_list.html'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        district = self.kwargs.get('slug')
        queryset = self.model.objects.filter(company__district__district__iexact=district)
        context['object_list'] = queryset
        user = self.request.user
        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        context['freq_categories'] = Category.objects.all().order_by('?')
        context['jobtype'] = JobType.objects.all()

        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        sss = District.objects.annotate(Count('company_detail_district__job_post_company')).order_by(
            '-company_detail_district__job_post_company__count')[:5]
        afd = []
        for i in sss:
            a = str(JobPost.objects.filter(company__district__district=i).count())
            aa = {'district': i.district, 'count': a}
            afd.append(aa)
        context['jbl'] = afd

        # a = self.paginate_queryset(queryset, 1)
        # print(type(a))
        # c = 0
        # for i in a:
        #     print(i)
        #     c = c + 1
        # context['page_range'] = int(c)

        return context


class JobTypeView(ListView):
    model = JobPost
    template_name = 'job_list.html'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)
        context['freq_categories'] = Category.objects.all().order_by('?')
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['jobtype'] = JobType.objects.all()

        jobtype = self.kwargs.get('slug')
        queryset = self.model.objects.filter(job_type__slug=jobtype)
        context['object_list'] = queryset
        for i in queryset:
            print(i)

        sss = District.objects.annotate(Count('company_detail_district__job_post_company')).order_by(
            '-company_detail_district__job_post_company__count')[:5]
        afd = []
        for i in sss:
            a = str(JobPost.objects.filter(company__district__district=i).count())
            aa = {'district': i.district, 'count': a}
            afd.append(aa)
        context['jbl'] = afd
        return context
