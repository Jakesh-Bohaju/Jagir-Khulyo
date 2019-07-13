from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView

from blog.models import *


# Create your views here.
class BlogListView(ListView):
    template_name = 'blog-home.html'
    model = Blog
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['blogs'] = Blog.objects.all()
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
        print(aaa.image)
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



