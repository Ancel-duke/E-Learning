from django.contrib import admin
from .models import Course, Lesson, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'difficulty', 'created_at', 'total_lessons', 'total_enrollments']
    list_filter = ['category', 'difficulty', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    readonly_fields = ['total_lessons', 'total_enrollments']
    date_hierarchy = 'created_at'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrollment_date', 'progress', 'completed']
    list_filter = ['enrollment_date', 'completed', 'course']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['enrollment_date']
    date_hierarchy = 'enrollment_date'
