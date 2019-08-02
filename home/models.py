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
        return self.slug

    def save(self, *args, **kwargs):
        value = self.category
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Province(models.Model):
    province_name = models.CharField(max_length=100)
    province_no = models.IntegerField()

    def __str__(self):
        return self.province_name


class District(models.Model):
    district = models.CharField(max_length=100)
    province_no = models.ForeignKey(Province, related_name='district_wise_province_no', on_delete=models.CASCADE)

    def __str__(self):
        return self.district


class JobType(models.Model):
    job_type = models.CharField(max_length=20)

    def __str__(self):
        return self.job_type


class JobLevel(models.Model):
    job_level = models.CharField(max_length=20)

    def __str__(self):
        return self.job_level


class FaqCompany(models.Model):
    company_question = models.CharField(max_length=200)
    company_answer = models.TextField()

    def __str__(self):
        return str(self.id)


class FaqSeeker(models.Model):
    seeker_question = models.CharField(max_length=200)
    seeker_answer = models.TextField()

    def __str__(self):
        return str(self.id)
