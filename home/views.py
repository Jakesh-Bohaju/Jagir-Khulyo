import datetime

from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView

from blog.models import Blog
from company.models import JobPost, Category, CompanyDetail, Faq, IPTracker
from home.models import JobType
from job_seeker.models import SeekerDetail


class IndexView(ListView):
    template_name = 'index.html'
    model = JobPost
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['jobs'] = JobPost.objects.all()
        context['jobtype'] = JobType.objects.all()
        context['categories'] = Category.objects.all().order_by('?')[:6]
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['latest_jobs'] = JobPost.objects.all().order_by('-id')
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['companies'] = CompanyDetail.objects.all()

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
        now1 = now + timezone.timedelta(hours=24)
        print(aa, now, now1)
        asd = IPTracker()
        obj = IPTracker.objects.filter(job_ip_id=x)
        temp = 0
        try:
            if obj.exists():
                for i in obj:
                    if i.ip_data == ip_data1:
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

        # try to save user ip with session 24 hours but not working
        # try:
        #     obj = IPTracker.objects.filter(job_ip_id=x)
        #     print(obj.count())
        #     if obj.exists():
        #         print("Yes I have data")
        #         for i in obj:
        #             print("DB time: ", i.date_time, "\ntimedelta 24hrs time :", now, i.ip_data, ip_data1)
        #
        #             if i.date_time < now:
        #                 print("I am gonna print")
        #                 asd.ip_data = ip_data1
        #                 asd.job_ip_id = request.POST.get('job')
        #                 asd.user_ip_id = request.POST.get('user')
        #                 asd.save()
        #             # else:
        #             # print(i.date_time, " is greater than ", now)
        #
        #
        #     else:
        #
        #         asd.ip_data = ip_data1
        #         asd.job_ip_id = request.POST.get('job')
        #         asd.user_ip_id = request.POST.get('user')
        #         asd.save()
        #
        # except Exception as e:
        #     print(e)

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
            search_set = search_set.filter(title__icontains=title, company__address__icontains=location,
                                           category__category__icontains=category)

        elif request.GET.get('title') and request.GET.get('location') or request.GET.get('category'):
            search_set = search_set.filter(title__icontains=title, company__address__icontains=location,
                                           category__category__icontains=category)

        elif request.GET.get('title') or request.GET.get('location') and request.GET.get('category'):
            search_set = search_set.filter(title__icontains=title, company__address__icontains=location,
                                           category__category__icontains=category)
        elif request.GET.get('title') or request.GET.get('location') or request.GET.get('category'):
            search_set = search_set.filter(title__icontains=title, company__address__icontains=location,
                                           category__category__icontains=category)

        # print(b)
        template_context = {
            'filtered_jobs': search_set,
            'top_jobs': JobPost.objects.all().order_by('?'),
            'latest_jobs': JobPost.objects.all().order_by('-id')[:6],
            'freq_categories': Category.objects.all().order_by('?')[:6],
            'blogs': Blog.objects.all().order_by('?')[:3],
            'job_by_locations': JobPost.objects.all(),
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
        user = self.request.user
        today = datetime.datetime.now()

        try:
            context['seeker'] = SeekerDetail.objects.get(user_id=user)
        except Exception as e:
            print(e)

        context['categories'] = Category.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['latest_jobs'] = JobPost.objects.all().order_by('-id')
        context['freq_categories'] = Category.objects.all().order_by('?')
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        return context


class CategoryListView(ListView):
    template_name = 'job_category.html'
    model = Category
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.all()
        user = self.request.user
        context['seeker'] = SeekerDetail.objects.get(user_id=user)
        context['freq_categories'] = Category.objects.all().order_by('?')
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        return context


class JobDetailView(DetailView):
    model = JobPost
    template_name = 'single_job.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        job = JobPost.objects.get(slug=slug)
        context['counts'] = IPTracker.objects.filter(job_ip__slug=slug).count()
        context['job'] = job
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['company'] = CompanyDetail.objects.get(job_post_company=job)
        user = self.request.user
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
