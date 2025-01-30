# profiles/admin.py

from django.contrib import admin
from .models import Donor, Needer

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'phone_number', 'address', 'registered_at')
    search_fields = ('user__username', 'blood_type', 'phone_number')
    list_filter = ('blood_type', 'registered_at')

@admin.register(Needer)
class NeederAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'phone_number', 'address', 'registered_at')
    search_fields = ('user__username', 'blood_type', 'phone_number')
    list_filter = ('blood_type', 'registered_at')
