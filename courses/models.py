from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('business', 'Business'),
        ('marketing', 'Marketing'),
        ('music', 'Music'),
        ('photography', 'Photography'),
        ('health', 'Health & Fitness'),
        ('language', 'Language'),
        ('other', 'Other'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def total_lessons(self):
        return self.lessons.count()
    
    @property
    def total_enrollments(self):
        return self.enrollments.count()

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True)
    materials = models.FileField(upload_to='lesson_materials/', blank=True, null=True)
    order = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - Lesson {self.order}: {self.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Progress percentage (0-100)"
    )
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
    
    def update_progress(self, new_progress):
        """Update progress and mark as completed if 100%"""
        self.progress = min(100, max(0, new_progress))
        if self.progress >= 100:
            self.completed = True
        self.save()
