# profiles/urls.py

from django.urls import path
from .views import (
    register_donor,
    register_needer,
    delete_donor,
    delete_needer,
    MatchingDonorsListView,
    MatchingNeedeersListView,
    donor_detail,
    needer_detail,
    find_doctor,
)
from .views import find_doctor

app_name = 'profiles'  # Add this line

urlpatterns = [
    path('register/donor/', register_donor, name='register_donor'),
    path('register/needer/', register_needer, name='register_needer'),
    path('doctor/find/', find_doctor, name='find_doctor'),
    path('donor/<int:pk>/', donor_detail, name='donor_detail'),
    path('needer/<int:pk>/', needer_detail, name='needer_detail'),
    path('donor/<int:pk>/delete/', delete_donor, name='delete_donor'),
    path('needer/<int:pk>/delete/', delete_needer, name='delete_needer'),
    path('needer/<int:needer_pk>/matching-donors/', MatchingDonorsListView.as_view(), name='matching_donors'),
    path('donor/<int:donor_pk>/matching-needeers/', MatchingNeedeersListView.as_view(), name='matching_needeers'),
]
