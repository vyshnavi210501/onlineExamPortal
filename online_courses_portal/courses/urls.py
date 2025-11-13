from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Instructor views
    path('my-courses/', views.MyCoursesListView.as_view(), name='my_courses'),
    path('create/', views.CourseCreateView.as_view(), name='create_course'),
    path('<slug:slug>/edit/', views.CourseUpdateView.as_view(), name='edit_course'),
    path('<slug:slug>/delete/', views.CourseDeleteView.as_view(), name='delete_course'),
    path('<slug:slug>/toggle-publish/', views.CourseTogglePublishView.as_view(), name='toggle_publish'),

    # Student views
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]