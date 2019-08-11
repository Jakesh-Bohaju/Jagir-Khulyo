from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

role = (
    ('company', 'Company'),
    ('job_seeker', 'Job Seeker')
)


class User(AbstractUser):
    role = models.CharField(choices=role, max_length=20)

    class Meta(AbstractUser.Meta):
        swappable = 'CUSTOM_AUTH_USER_MODEL'


