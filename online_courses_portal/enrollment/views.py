from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.utils.decorators import method_decorator
from dashboard.decorators import student_required
from .models import Enrollment
from courses.models import Course


@method_decorator(student_required, name='dispatch')
class EnrollView(LoginRequiredMixin, View):
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_published=True)
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'status': 'Active'}
        )
        if created:
            messages.success(request, 'Successfully enrolled in the course!')
        else:
            messages.info(request, 'Already Enrolled')
        return redirect('enrollment:my_courses')


@method_decorator(student_required, name='dispatch')
class MyEnrolledCoursesView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'enrollment/my_courses.html'
    context_object_name = 'enrollments'
    ordering = ['-enrolled_at']

    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user,
            status='Active'
        ).select_related('course__instructor', 'course__category')
