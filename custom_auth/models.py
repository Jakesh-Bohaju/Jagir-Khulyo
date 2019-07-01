from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

role = (
    ('company', 'Company'),
    ('job_seeker', 'Job Seeker')
)


class User(AbstractUser):
    role = models.CharField(choices=role, max_length=20)

    class Meta(AbstractUser.Meta):
        swappable = 'CUSTOM_AUTH_USER_MODEL'
