from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import RegistrationForm,LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from .models import User
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
    def get_success_url(self):
        user = self.request.user
        # Redirect based on role
        if user.role == 'admin':
            return '/admin/'
        elif user.role == 'instructor':
            return '/instructor/dashboard/'
        else:
            return '/student/dashboard/'

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return render(request, 'accounts/logout.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')   