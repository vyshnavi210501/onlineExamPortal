from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class InstructorDashboardView(TemplateView):
    template_name="dashboard/instructor.html"
    
class StudentDashboardView(TemplateView):
    template_name="dashboard/student.html"
