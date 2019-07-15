from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify
from sorl.thumbnail import ImageField
from custom_auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=100)
    published_date = models.DateField(auto_now=True)
    author = models.CharField(max_length=50)
    content = RichTextField()
    image = ImageField()
    slug = models.SlugField()

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Comment(models.Model):
    answer = RichTextField()
    comment_date = models.DateField(auto_now=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='sub_comments', on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        value = self.comment_user.username + ' ' + self.answer
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


#
# class Reply(models.Model):
#     reply = RichTextField()
#     reply_date = models.DateField(auto_now=True)
#     reply_blog = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     reply_user = models.ForeignKey(User, on_delete=models.CASCADE)
