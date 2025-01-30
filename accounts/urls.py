from django.urls import path
from .views import register_view, CustomLoginView
from django.contrib.auth.views import LogoutView
from .views import register_view, CustomLoginView, logout_view
from .views import resource_center

app_name = 'accounts'  # Add this line

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('resource-center/', resource_center, name='resource_center'),
]