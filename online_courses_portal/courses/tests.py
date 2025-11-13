from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Course, Category

User = get_user_model()


class CourseTests(TestCase):
    def setUp(self):
        # Create users
        self.instructor = User.objects.create_user(username='instructor', password='pass', role='instructor')
        self.student = User.objects.create_user(username='student', password='pass', role='student')
        self.other_instructor = User.objects.create_user(username='other_instructor', password='pass', role='instructor')

        # Create category
        self.category = Category.objects.create(name='Programming', slug='programming')

        # Create course
        self.course = Course.objects.create(
            title='Python Basics',
            short_description='Learn Python',
            full_description='Detailed Python course',
            instructor=self.instructor,
            category=self.category,
            is_published=True
        )

    def test_instructor_can_create_course(self):
        self.client.login(username='instructor', password='pass')
        response = self.client.post(reverse('courses:create_course'), {
            'title': 'New Course',
            'short_description': 'Short desc',
            'full_description': 'Full desc',
            'category': self.category.id,
            'is_published': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Course.objects.filter(title='New Course', instructor=self.instructor).exists())

    def test_student_cannot_create_course(self):
        self.client.login(username='student', password='pass')
        response = self.client.post(reverse('courses:create_course'), {
            'title': 'New Course',
            'short_description': 'Short desc',
            'full_description': 'Full desc',
            'category': self.category.id,
            'is_published': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login or dashboard

    def test_instructor_can_edit_own_course(self):
        self.client.login(username='instructor', password='pass')
        response = self.client.post(reverse('courses:edit_course', kwargs={'slug': self.course.slug}), {
            'title': 'Updated Python Basics',
            'short_description': 'Learn Python',
            'full_description': 'Detailed Python course',
            'category': self.category.id,
            'is_published': True
        })
        self.assertEqual(response.status_code, 302)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Python Basics')

    def test_instructor_cannot_edit_other_course(self):
        self.client.login(username='other_instructor', password='pass')
        response = self.client.post(reverse('courses:edit_course', kwargs={'slug': self.course.slug}), {
            'title': 'Hacked Title',
            'short_description': 'Learn Python',
            'full_description': 'Detailed Python course',
            'category': self.category.id,
            'is_published': True
        })
        self.assertEqual(response.status_code, 404)  # Not found because ownership check

    def test_instructor_can_delete_own_course(self):
        self.client.login(username='instructor', password='pass')
        response = self.client.post(reverse('courses:delete_course', kwargs={'slug': self.course.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Course.objects.filter(slug=self.course.slug).exists())

    def test_student_can_view_published_course(self):
        self.client.login(username='student', password='pass')
        response = self.client.get(reverse('courses:course_detail', kwargs={'slug': self.course.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Basics')

    def test_student_cannot_view_unpublished_course(self):
        self.course.is_published = False
        self.course.save()
        self.client.login(username='student', password='pass')
        response = self.client.get(reverse('courses:course_detail', kwargs={'slug': self.course.slug}))
        self.assertEqual(response.status_code, 404)

    def test_course_list_shows_only_published(self):
        unpublished_course = Course.objects.create(
            title='Unpublished',
            short_description='Not visible',
            full_description='Not visible',
            instructor=self.instructor,
            is_published=False
        )
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Basics')
        self.assertNotContains(response, 'Unpublished')
