from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from .decorators import instructor_required, student_required
from courses.models import Course
from enrollment.models import Enrollment

# Create your views here.
@method_decorator(instructor_required, name='dispatch')
class InstructorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/instructor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(instructor=self.request.user).select_related('category').order_by('-created_at')
        return context

@method_decorator(student_required, name='dispatch')
class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/student.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollments = Enrollment.objects.filter(student=self.request.user).select_related('course__instructor', 'course__category')
        context['courses'] = [enrollment.course for enrollment in enrollments]
        return context
