from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User,Profile


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Allow only Student or Instructor roles during registration
        self.fields['role'].choices = [
            (choice, label)
            for choice, label in User.role_choices
            if choice in ['student', 'instructor']
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="username")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'contact_number']