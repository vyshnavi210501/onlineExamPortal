from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import RegistrationForm,LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
# Create your views here.
class RegistrationView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Registration successful. Please log in.")
        return redirect('login')

class LoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('profile')

class LogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    success_url = reverse_lazy('logout')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')   