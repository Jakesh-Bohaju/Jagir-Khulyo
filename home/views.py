from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from blog.models import Blog
from company.models import JobPost, Category, CompanyDetail, Faq, IPTracker


class IndexView(ListView):
    template_name = 'index.html'
    model = JobPost
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['jobs'] = JobPost.objects.all()
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

        asd = IPTracker()
        asd.ip_data = ip_data1
        asd.job_ip_id = request.POST.get('job')
        asd.user_ip_id = request.POST.get('user')
        asd.save()

        return redirect('/seeker/' + a.slug)


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


class FaqView(TemplateView):
    template_name = 'faq.html'
    model = Faq

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sfaqs'] = Faq.objects.filter(role='job_seeker')
        context['cfaqs'] = Faq.objects.filter(role='company')

        return context
