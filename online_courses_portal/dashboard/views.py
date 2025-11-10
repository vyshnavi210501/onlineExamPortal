from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from .decorators import instructor_required, student_required

# Create your views here.
@method_decorator(instructor_required, name='dispatch')
class InstructorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/instructor.html"

@method_decorator(student_required, name='dispatch')
class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/student.html"
