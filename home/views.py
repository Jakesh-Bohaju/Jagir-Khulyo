from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, ListView

from company.models import JobPost, Category


class IndexView(TemplateView):
    template_name = 'index.html'


class SearchView(ListView):
    template_name = 'search_result.html'
    model = JobPost

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title')
        location = request.GET.get('location')
        category = request.GET.get('category')
        search_set = JobPost.objects.filter()
        # b = []
        if request.GET.get('title') and request.GET.get('location') and request.GET.get('category'):
            search_set = search_set.filter(title__icontains=title, company__address__icontains=location,
                                           category__category__icontains=category)
            # b.append(search_set)

        # print(b)
        template_context = {
            'filtered_jobs': search_set,
            'top_jobs': JobPost.objects.all().order_by('?')[:6],
            'latest_jobs': JobPost.objects.all().order_by('-id')[:6],
            'freq_categories': Category.objects.all().order_by('?')[:6],
        }
        return render(request, 'search_result.html', template_context)
