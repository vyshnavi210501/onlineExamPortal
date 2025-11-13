from django.db import models

# Create your models here.
class Enrollment(models.Model):
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Active')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"