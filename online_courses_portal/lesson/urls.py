from django.urls import path
from . import views

app_name = 'lesson'

urlpatterns = [
    path('course/<slug:slug>/lessons/', views.CourseLessonsView.as_view(), name='course_lessons'),
]