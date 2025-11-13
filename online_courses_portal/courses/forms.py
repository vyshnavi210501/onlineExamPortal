from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'short_description', 'full_description', 'category',
            'thumbnail', 'resource_file', 'is_published'
        ]
        widgets = {
            'short_description': forms.TextInput(attrs={'placeholder': 'Brief summary of the course'}),
            'full_description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Detailed course description'}),
            'thumbnail': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'resource_file': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,.zip'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.instructor = self.user
        if commit:
            instance.save()
        return instance