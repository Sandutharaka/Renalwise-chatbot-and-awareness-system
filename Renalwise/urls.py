# Renalwise/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from profiles import views as profile_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('community/', include('community.urls', namespace='community')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
]
