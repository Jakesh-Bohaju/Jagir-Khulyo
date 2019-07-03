from django.utils.text import slugify

from custom_auth.models import User
from django.db import models

# Create your models here.
from home.models import *
from job_seeker.models import SeekerDetail


class CompanyDetail(models.Model):
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=50)
    company_type = models.CharField(max_length=100)
    phone_no = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name


class JobPost(models.Model):
    title = models.CharField(max_length=100)
    job_level = models.CharField(max_length=15)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vacancy_no = models.IntegerField()
    experience = models.CharField(max_length=15)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    salary = models.IntegerField()
    description = models.TextField()
    pub_date = models.DateField(auto_now=True)
    deadline = models.DateField()
    company = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.slug + '-' + self.company

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class ReceivedResume(models.Model):
    job_title = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applicant_name = models.ForeignKey(SeekerDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.applicant_name
