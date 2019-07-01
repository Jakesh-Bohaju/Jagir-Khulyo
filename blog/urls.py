from django.urls import path

from blog.views import *

app_name = 'blog'
urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>', BlogDetailView.as_view(), name='single_blog')
]
