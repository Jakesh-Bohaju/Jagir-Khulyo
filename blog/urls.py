from django.urls import path

from blog.views import *
from blog.views import CommentView

app_name = 'blog'
urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>', BlogDetailView.as_view(), name='single_blog'),
    path('comment/', CommentView.as_view()),
]
