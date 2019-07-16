from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, ListView
from rest_framework import generics, serializers

from blog.models import Blog, Comment
from company.models import JobPost, Category, CompanyDetail
from custom_auth.models import User


class IndexView(ListView):
    template_name = 'index.html'
    model = JobPost
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['jobs'] = JobPost.objects.all()
        context['categories'] = Category.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['latest_jobs'] = JobPost.objects.all().order_by('-id')
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['companies'] = CompanyDetail.objects.all()

        return context


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
            'top_jobs': JobPost.objects.all().order_by('?')[:6],
            'latest_jobs': JobPost.objects.all().order_by('-id')[:6],
            'freq_categories': Category.objects.all().order_by('?')[:6],
        }
        return render(request, 'search_result.html', template_context)


class Error404(TemplateView):
    template_name = 'error_404.html'

