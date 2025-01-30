from django import forms
from .models import Donor, Needer, BloodType

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['phone_number', 'blood_type', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'}),
            'blood_type': forms.Select(choices=BloodType.choices, attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter your address', 'rows': 3, 'class': 'form-control'}),
        }

class NeederForm(forms.ModelForm):
    class Meta:
        model = Needer
        fields = ['phone_number', 'blood_type', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'}),
            'blood_type': forms.Select(choices=BloodType.choices, attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter your address', 'rows': 3, 'class': 'form-control'}),
        }

class FindDoctorForm(forms.Form):
    city = forms.CharField(
        label='City',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city name'})
    )