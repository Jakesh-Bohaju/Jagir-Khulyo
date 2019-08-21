from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.template import loader
from django.views.generic import ListView, CreateView
from rest_framework import generics

from blog.models import *
# Create your views here.
from blog.serializer import CommentSerializer
from company.models import JobPost


class BlogListView(ListView):
    template_name = 'blog-home.html'
    model = Blog
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['blogs'] = Blog.objects.all()
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')

        return context


class BlogDetailView(CreateView):
    template_name = 'blog-single.html'
    model = Comment
    fields = ['answer']

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context = super().get_context_data(**kwargs)
        aaa = Blog.objects.get(slug=slug)
        context['blog'] = aaa
        context['blogs'] = Blog.objects.all().order_by('?')[:3]
        context['job_by_locations'] = JobPost.objects.all()
        context['top_jobs'] = JobPost.objects.all().order_by('?')
        context['comments'] = Comment.objects.filter(parent_id=None, blog_id=aaa.id)
        context['reply'] = Comment.objects.filter(blog_id=aaa.id)

        return context

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        aaa = Blog.objects.get(slug=slug)

        form = self.get_form()

        if form.is_valid():
            a = form.save(commit=False)
            a.comment_user = request.user
            z = request.POST.get('comment_id')
            if z:
                a.parent_id = z

            a.blog_id = aaa.id
            a.save()
            # return to same page
            return HttpResponseRedirect(self.request.path_info)
        return HttpResponseRedirect(self.request.path_info)


class CommentView(generics.ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = CommentSerializer

#
# def lazy_load_posts(request):
#     page = request.POST.get('page')
#     posts = Comment.objects.all()
#
#     # use Django's pagination
#     # https://docs.djangoproject.com/en/dev/topics/pagination/
#     results_per_page = 5
#     paginator = Paginator(posts, results_per_page)
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(2)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     # build a html posts list with the paginated posts
#     posts_html = loader.render_to_string('comment.html', {'posts': posts})
