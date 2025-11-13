#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_courses_portal.settings')
django.setup()

from courses.models import Category, Course
from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_data():
    # Create categories
    categories_data = [
        'Programming',
        'Data Science',
        'Web Development',
        'Machine Learning',
        'Design'
    ]

    categories = []
    for name in categories_data:
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={'slug': ''}
        )
        categories.append(category)
        print(f"Created category: {category.name} (slug: {category.slug})")

    # Create instructor if not exists
    instructor, created = User.objects.get_or_create(
        username='test_instructor',
        defaults={
            'email': 'instructor@test.com',
            'role': 'instructor'
        }
    )
    if created:
        instructor.set_password('password123')
        instructor.save()
        print("Created instructor: test_instructor")

    # Create courses
    courses_data = [
        ('Python Basics', 'Learn Python programming fundamentals', 'Complete guide to Python basics including variables, loops, and functions.', categories[0]),
        ('Django Web Development', 'Build web apps with Django', 'Master Django framework for full-stack web development.', categories[0]),
        ('Data Science with Python', 'Analyze data with Python', 'Learn pandas, numpy, and matplotlib for data analysis.', categories[1]),
        ('Machine Learning Fundamentals', 'Introduction to ML', 'Understand core machine learning concepts and algorithms.', categories[3]),
        ('UI/UX Design Principles', 'Design beautiful interfaces', 'Learn design principles for creating user-friendly interfaces.', categories[4]),
    ]

    for title, short_desc, full_desc, category in courses_data:
        course, created = Course.objects.get_or_create(
            title=title,
            defaults={
                'short_description': short_desc,
                'full_description': full_desc,
                'instructor': instructor,
                'category': category,
                'is_published': True,
                'slug': ''
            }
        )
        print(f"Created course: {course.title} (slug: {course.slug})")

    print("\nTest data created successfully!")
    print(f"Categories: {Category.objects.count()}")
    print(f"Courses: {Course.objects.count()}")

if __name__ == '__main__':
    create_test_data()