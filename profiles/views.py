# profiles/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DonorForm, NeederForm
from .models import Donor, Needer, BloodType
from django.views.generic import ListView
import requests
from django.shortcuts import render
from django.conf import settings
from .forms import FindDoctorForm
import json

@login_required
def register_donor(request):
    """
    If the user already has a Needer profile, we show them all Donors who share that blood type.
    They cannot register as a Donor in that case.

    Otherwise, we allow the user to create/edit/delete their Donor profile.
    """
    # If user is a Needer => show matched Donors
    if hasattr(request.user, 'needer_profile'):
        needer_profile = request.user.needer_profile
        # Retrieve all donors with the same blood type
        matching_donors = Donor.objects.filter(blood_type=needer_profile.blood_type)

        return render(request, 'profiles/matched_donors.html', {
            'matching_donors': matching_donors,
            'blood_type': needer_profile.blood_type
        })

    # Otherwise, proceed with donor registration logic
    donor_profile = getattr(request.user, 'donor_profile', None)

    if request.method == 'POST':
        # check for delete
        if 'delete' in request.POST and donor_profile:
            donor_profile.delete()
            messages.success(request, 'Donor registration deleted.')
            return redirect('home')

        form = DonorForm(request.POST, instance=donor_profile)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            messages.success(request, 'Donor information saved successfully!')
            return redirect('profiles:register_donor')
    else:
        form = DonorForm(instance=donor_profile)

    return render(request, 'profiles/register_donor.html', {
        'form': form,
        'donor_profile': donor_profile,
    })

@login_required
def register_needer(request):
    """
    If the user already has a Donor profile, we show them all Needeers who share that blood type.
    They cannot register as a Needer in that case.

    Otherwise, we allow the user to create/edit/delete their Needer profile.
    """
    # If user is a Donor => show matched Needeers
    if hasattr(request.user, 'donor_profile'):
        donor_profile = request.user.donor_profile
        # Retrieve all needeers with the same blood type
        matching_needeers = Needer.objects.filter(blood_type=donor_profile.blood_type)

        return render(request, 'profiles/matched_needeers.html', {
            'matching_needeers': matching_needeers,
            'blood_type': donor_profile.blood_type
        })

    # Otherwise, proceed with needer registration logic
    needer_profile = getattr(request.user, 'needer_profile', None)

    if request.method == 'POST':
        if 'delete' in request.POST and needer_profile:
            needer_profile.delete()
            messages.success(request, 'Needer registration deleted.')
            return redirect('home')

        form = NeederForm(request.POST, instance=needer_profile)
        if form.is_valid():
            needer = form.save(commit=False)
            needer.user = request.user
            needer.save()
            messages.success(request, 'Needer information saved successfully!')
            return redirect('profiles:register_needer')
    else:
        form = NeederForm(instance=needer_profile)

    return render(request, 'profiles/register_needer.html', {
        'form': form,
        'needer_profile': needer_profile,
    })


@login_required
def delete_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk, user=request.user)
    if request.method == 'POST':
        donor.delete()
        messages.success(request, 'Your Donor registration has been deleted.')
        return redirect('home')
    return render(request, 'profiles/confirm_delete.html', {'object': donor, 'type': 'donor'})

@login_required
def delete_needer(request, pk):
    needer = get_object_or_404(Needer, pk=pk, user=request.user)
    if request.method == 'POST':
        needer.delete()
        messages.success(request, 'Your Needer registration has been deleted.')
        return redirect('home')
    return render(request, 'profiles/confirm_delete.html', {'object': needer, 'type': 'needer'})

class MatchingDonorsListView(ListView):
    model = Donor
    template_name = 'profiles/matching_donors.html'
    context_object_name = 'donors'
    
    def get_queryset(self):
        needer_id = self.kwargs.get('needer_pk')
        needer = get_object_or_404(Needer, pk=needer_id)
        return Donor.objects.filter(blood_type=needer.blood_type)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        needer_id = self.kwargs.get('needer_pk')
        context['needer'] = get_object_or_404(Needer, pk=needer_id)
        return context

class MatchingNeedeersListView(ListView):
    model = Needer
    template_name = 'profiles/matching_needeers.html'
    context_object_name = 'needeers'
    
    def get_queryset(self):
        donor_id = self.kwargs.get('donor_pk')
        donor = get_object_or_404(Donor, pk=donor_id)
        return Needer.objects.filter(blood_type=donor.blood_type)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        donor_id = self.kwargs.get('donor_pk')
        context['donor'] = get_object_or_404(Donor, pk=donor_id)
        return context

@login_required
def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk, user=request.user)
    return render(request, 'profiles/donor_detail.html', {'donor': donor})

@login_required
def needer_detail(request, pk):
    needer = get_object_or_404(Needer, pk=pk, user=request.user)
    return render(request, 'profiles/needer_detail.html', {'needer': needer})

def find_doctor(request):
    results = []
    city_name = ""

    if request.method == "POST":
        city_name = request.POST.get('city_name', '').strip()
        if city_name:
            # Prepare API request
            url = "https://google.serper.dev/places"
            payload = {
                "q": f"Kidney Doctor in {city_name}",
                "location": "Sri Lanka",
                "gl": "lk"
            }
            headers = {
                'X-API-KEY': 'b7491f45519688b417ae96a87efb6bca1fb8f944',
                'Content-Type': 'application/json'
            }

            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("places", [])
                    if not results:
                        messages.warning(request, "No doctors found for that city.")
                else:
                    messages.error(request, f"Error: {response.status_code} from API.")
            except Exception as e:
                messages.error(request, f"API request failed: {e}")
        else:
            messages.warning(request, "Please enter a city name.")

    return render(request, 'profiles/doctor/find_doctor.html', {
        'results': results,
        'city_name': city_name,
    })