from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.username
