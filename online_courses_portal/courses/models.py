from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"


class Course(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    resource_file = models.FileField(upload_to='course_resources/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Course.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()
    video_url = models.URLField(blank=True, null=True)
    attachment = models.FileField(upload_to='lesson_attachments/', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['order']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    courses = models.ManyToManyField(Course, related_name='tags', blank=True)

    def __str__(self):
        return self.name
