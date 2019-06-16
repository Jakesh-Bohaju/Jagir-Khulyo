from django.db import models


# Create your models here.
class Education(models.Model):
    education = models.CharField(max_length=50)


class Gender(models.Model):
    gender = models.CharField(max_length=15)


class Category(models.Model):
    category = models.CharField(max_length=50)
