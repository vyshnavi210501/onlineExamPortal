from django.urls import path
from . import views

app_name = 'enrollment'

urlpatterns = [
    path('enroll/<slug:slug>/', views.EnrollView.as_view(), name='enroll'),
    path('my-courses/', views.MyEnrolledCoursesView.as_view(), name='my_courses'),
]