from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import RegistrationForm,LoginForm,ProfileForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,DetailView,UpdateView
from .models import User,Profile
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
            return reverse_lazy('admin:index')
        elif user.role == 'instructor':
            return reverse_lazy('instructor_dashboard')
        else:
            return reverse_lazy('student_dashboard')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return render(request, 'accounts/logout.html')


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    model = Profile

    def get_object(self):
        return self.request.user.profile


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit_profile.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile