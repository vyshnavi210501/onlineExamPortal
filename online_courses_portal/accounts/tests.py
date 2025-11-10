from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Profile

User = get_user_model()

class RoleBasedAccessTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.student = User.objects.create_user(
            username='student1',
            email='student@example.com',
            password='password123',
            role='student'
        )
        self.instructor = User.objects.create_user(
            username='instructor1',
            email='instructor@example.com',
            password='password123',
            role='instructor'
        )
        self.admin = User.objects.create_user(
            username='admin1',
            email='admin@example.com',
            password='password123',
            role='admin'
        )
        self.client = Client()

    def test_student_dashboard_access(self):
        # Test student can access their dashboard
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)

        # Test instructor cannot access student dashboard
        self.client.login(username='instructor1', password='password123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect due to decorator

    def test_instructor_dashboard_access(self):
        # Test instructor can access their dashboard
        self.client.login(username='instructor1', password='password123')
        response = self.client.get(reverse('instructor_dashboard'))
        self.assertEqual(response.status_code, 200)

        # Test student cannot access instructor dashboard
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('instructor_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect due to decorator

    def test_unauthenticated_access(self):
        # Test unauthenticated user cannot access dashboards
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        response = self.client.get(reverse('instructor_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_creation_signal(self):
        # Test that Profile is created automatically when User is created
        self.assertTrue(hasattr(self.student, 'profile'))
        self.assertIsInstance(self.student.profile, Profile)

    def test_profile_view_access(self):
        # Test authenticated users can access profile
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_access(self):
        # Test authenticated users can access profile edit
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
