from django.urls import path
from .views import (
    CourseListCreateView,
    CourseDetailView,
    LessonListCreateView,
    LessonDetailView,
    EnrollmentListView,
    EnrollmentCreateView,
    EnrollmentDetailView,
    ProgressUpdateView,
    CourseEnrollView,
    InstructorCoursesView
)

urlpatterns = [
    # Course endpoints
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/enroll/', CourseEnrollView.as_view(), name='course-enroll'),
    path('instructor/courses/', InstructorCoursesView.as_view(), name='instructor-courses'),
    
    # Lesson endpoints
    path('courses/<int:course_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    
    # Enrollment endpoints
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/create/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('enrollments/<int:pk>/progress/', ProgressUpdateView.as_view(), name='progress-update'),
]
