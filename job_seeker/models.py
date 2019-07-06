from custom_auth.models import User
from django.db import models

# Create your models here.
from home.models import *
from sorl.thumbnail import ImageField


class SeekerDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/', verbose_name="")
    image = ImageField(upload_to='job_seeker/', verbose_name="")
    slug = models.SlugField()

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

