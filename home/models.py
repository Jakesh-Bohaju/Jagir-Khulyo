from django.db import models


# Create your models here.
from django.utils.text import slugify


class Education(models.Model):
    education = models.CharField(max_length=50)

    def __str__(self):
        return self.education


class Gender(models.Model):
    gender = models.CharField(max_length=15)

    def __str__(self):
        return self.gender


class Category(models.Model):
    category = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        value = self.category
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
