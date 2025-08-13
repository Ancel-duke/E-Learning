from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Course, Lesson, Enrollment
from accounts.models import UserProfile

class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.user.profile.user_type = 'instructor'
        self.user.profile.save()
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            category='programming',
            difficulty='beginner',
            instructor=self.user
        )
    
    def test_course_creation(self):
        """Test course creation"""
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(self.course.instructor, self.user)
        self.assertEqual(self.course.total_lessons, 0)
        self.assertEqual(self.course.total_enrollments, 0)
    
    def test_course_string_representation(self):
        """Test course string representation"""
        self.assertEqual(str(self.course), 'Test Course')

class LessonModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.user.profile.user_type = 'instructor'
        self.user.profile.save()
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            category='programming',
            difficulty='beginner',
            instructor=self.user
        )
        
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            video_url='https://example.com/video',
            order=1
        )
    
    def test_lesson_creation(self):
        """Test lesson creation"""
        self.assertEqual(self.lesson.title, 'Test Lesson')
        self.assertEqual(self.lesson.course, self.course)
        self.assertEqual(self.lesson.order, 1)
    
    def test_lesson_string_representation(self):
        """Test lesson string representation"""
        expected = f"{self.course.title} - Lesson {self.lesson.order}: {self.lesson.title}"
        self.assertEqual(str(self.lesson), expected)

class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.instructor.profile.user_type = 'instructor'
        self.instructor.profile.save()
        
        self.student = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            category='programming',
            difficulty='beginner',
            instructor=self.instructor
        )
        
        self.enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            progress=50
        )
    
    def test_enrollment_creation(self):
        """Test enrollment creation"""
        self.assertEqual(self.enrollment.user, self.student)
        self.assertEqual(self.enrollment.course, self.course)
        self.assertEqual(self.enrollment.progress, 50)
        self.assertFalse(self.enrollment.completed)
    
    def test_enrollment_progress_update(self):
        """Test enrollment progress update"""
        self.enrollment.update_progress(100)
        self.assertEqual(self.enrollment.progress, 100)
        self.assertTrue(self.enrollment.completed)
    
    def test_enrollment_string_representation(self):
        """Test enrollment string representation"""
        expected = f"{self.student.username} enrolled in {self.course.title}"
        self.assertEqual(str(self.enrollment), expected)

class CoursesAPITest(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.instructor.profile.user_type = 'instructor'
        self.instructor.profile.save()
        
        self.student = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            category='programming',
            difficulty='beginner',
            instructor=self.instructor
        )
        
        self.course_list_url = reverse('course-list-create')
        self.course_detail_url = reverse('course-detail', args=[self.course.id])
        self.course_enroll_url = reverse('course-enroll', args=[self.course.id])
    
    def test_course_list_unauthorized(self):
        """Test course list without authentication"""
        response = self.client.get(self.course_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_course_create_as_instructor(self):
        """Test course creation as instructor"""
        self.client.force_authenticate(user=self.instructor)
        
        course_data = {
            'title': 'New Course',
            'description': 'New Description',
            'category': 'design',
            'difficulty': 'intermediate'
        }
        
        response = self.client.post(self.course_list_url, course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
    
    def test_course_create_as_student(self):
        """Test course creation as student (should fail)"""
        self.client.force_authenticate(user=self.student)
        
        course_data = {
            'title': 'New Course',
            'description': 'New Description',
            'category': 'design',
            'difficulty': 'intermediate'
        }
        
        response = self.client.post(self.course_list_url, course_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_course_detail(self):
        """Test course detail retrieval"""
        response = self.client.get(self.course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Course')
    
    def test_course_update_as_instructor(self):
        """Test course update as instructor"""
        self.client.force_authenticate(user=self.instructor)
        
        update_data = {
            'title': 'Updated Course'
        }
        
        response = self.client.patch(self.course_detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Course')
    
    def test_course_enroll(self):
        """Test course enrollment"""
        self.client.force_authenticate(user=self.student)
        
        response = self.client.post(self.course_enroll_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)
    
    def test_course_enroll_duplicate(self):
        """Test duplicate course enrollment"""
        # Create enrollment first
        Enrollment.objects.create(user=self.student, course=self.course)
        
        self.client.force_authenticate(user=self.student)
        response = self.client.post(self.course_enroll_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LessonAPITest(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.instructor.profile.user_type = 'instructor'
        self.instructor.profile.save()
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            category='programming',
            difficulty='beginner',
            instructor=self.instructor
        )
        
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            video_url='https://example.com/video',
            order=1
        )
        
        self.lesson_list_url = reverse('lesson-list-create', args=[self.course.id])
        self.lesson_detail_url = reverse('lesson-detail', args=[self.lesson.id])
    
    def test_lesson_list(self):
        """Test lesson list retrieval"""
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_lesson_create_as_instructor(self):
        """Test lesson creation as instructor"""
        self.client.force_authenticate(user=self.instructor)
        
        lesson_data = {
            'title': 'New Lesson',
            'video_url': 'https://example.com/new-video',
            'order': 2
        }
        
        response = self.client.post(self.lesson_list_url, lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
    
    def test_lesson_detail(self):
        """Test lesson detail retrieval"""
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')

class EnrollmentAPITest(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.instructor.profile.user_type = 'instructor'
        self.instructor.profile.save()
        
        self.student = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            category='programming',
            difficulty='beginner',
            instructor=self.instructor
        )
        
        self.enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            progress=50
        )
        
        self.enrollment_list_url = reverse('enrollment-list')
        self.enrollment_detail_url = reverse('enrollment-detail', args=[self.enrollment.id])
        self.progress_update_url = reverse('progress-update', args=[self.enrollment.id])
    
    def test_enrollment_list_as_student(self):
        """Test enrollment list as student"""
        self.client.force_authenticate(user=self.student)
        
        response = self.client.get(self.enrollment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_enrollment_detail(self):
        """Test enrollment detail retrieval"""
        self.client.force_authenticate(user=self.student)
        
        response = self.client.get(self.enrollment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['progress'], 50)
    
    def test_progress_update(self):
        """Test progress update"""
        self.client.force_authenticate(user=self.student)
        
        progress_data = {
            'progress': 75
        }
        
        response = self.client.patch(self.progress_update_url, progress_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.progress, 75)
    
    def test_progress_update_completion(self):
        """Test progress update to completion"""
        self.client.force_authenticate(user=self.student)
        
        progress_data = {
            'progress': 100
        }
        
        response = self.client.patch(self.progress_update_url, progress_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.progress, 100)
        self.assertTrue(self.enrollment.completed)
