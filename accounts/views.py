from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in upon successful registration
            login(request, user)
            return redirect('home')  # or wherever you want to redirect
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')  # or wherever you want to go after login

@login_required
def logout_view(request):
    """
    Logs out the user via POST.
    Shows a simple confirmation or logs out immediately.
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        return redirect('home')  # or 'accounts:login'

    # If GET, show a confirmation template (optional)
    return render(request, 'accounts/logout_confirm.html')

def resource_center(request):
    return render(request, 'resource_center.html')