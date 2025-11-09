from django.urls import path
from .views import InstructorDashboardView, StudentDashboardView

urlpatterns = [
    # Define your dashboard URLs here
    path('instructor/dashboard/', InstructorDashboardView.as_view(), name='instructor_dashboard'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
]