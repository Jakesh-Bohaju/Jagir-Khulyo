from custom_auth.models import User
from django.db import models

# Create your models here.
from home.models import *


class CompanyDetail(models.Model):
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=50)
    company_type = models.CharField(max_length=100)
    phone_no = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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



