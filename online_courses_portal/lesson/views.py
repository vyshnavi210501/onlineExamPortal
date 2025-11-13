from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from dashboard.decorators import student_required
from .models import Lesson
from courses.models import Course
from enrollment.models import Enrollment


@method_decorator(student_required, name='dispatch')
class CourseLessonsView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'lesson/course_lessons.html'
    context_object_name = 'lessons'
    ordering = ['order']

    def get(self, request, *args, **kwargs):
        course_slug = self.kwargs['slug']
        course = get_object_or_404(Course, slug=course_slug)
        if not Enrollment.objects.filter(student=request.user, course=course, status='Active').exists():
            messages.error(request, 'You are not enrolled in this course.')
            return redirect('courses:course_detail', slug=course_slug)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        course_slug = self.kwargs['slug']
        course = get_object_or_404(Course, slug=course_slug)
        return Lesson.objects.filter(course=course).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = self.kwargs['slug']
        context['course'] = get_object_or_404(Course, slug=course_slug)
        return context
