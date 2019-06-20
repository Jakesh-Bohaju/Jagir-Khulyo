from custom_auth.models import User
from django.db import models

# Create your models here.
from home.models import *


class SeekerDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/', verbose_name="")

    def __str__(self):
        return self.name

