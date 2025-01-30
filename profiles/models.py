# profiles/models.py

from django.db import models
from django.conf import settings
from django.urls import reverse

class BloodType(models.TextChoices):
    O_POSITIVE = 'O+', 'O+'
    O_NEGATIVE = 'O-', 'O-'
    A_POSITIVE = 'A+', 'A+'
    A_NEGATIVE = 'A-', 'A-'
    B_POSITIVE = 'B+', 'B+'
    B_NEGATIVE = 'B-', 'B-'
    AB_POSITIVE = 'AB+', 'AB+'
    AB_NEGATIVE = 'AB-', 'AB-'

class Donor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donor_profile'
    )
    phone_number = models.CharField(max_length=15)
    blood_type = models.CharField(max_length=3, choices=BloodType.choices)
    address = models.TextField()
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Donor: {self.user.username} ({self.blood_type})'

class Needer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='needer_profile'
    )
    phone_number = models.CharField(max_length=15)
    blood_type = models.CharField(max_length=3, choices=BloodType.choices)
    address = models.TextField()
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Needer: {self.user.username} ({self.blood_type})'
