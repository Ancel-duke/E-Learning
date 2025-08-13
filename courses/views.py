from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Enrollment
from .serializers import (
    CourseSerializer, CourseCreateSerializer,
    LessonSerializer, LessonCreateSerializer,
    EnrollmentSerializer, EnrollmentCreateSerializer,
    ProgressUpdateSerializer
)
from .permissions import (
    IsInstructorOrReadOnly, IsCourseInstructorOrReadOnly,
    IsLessonInstructorOrReadOnly, IsEnrollmentOwnerOrReadOnly
)

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'instructor']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'total_enrollments']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateSerializer
        return CourseSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInstructorOrReadOnly()]
        return [permissions.AllowAny()]

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsCourseInstructorOrReadOnly]

class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOrReadOnly]
    
    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Lesson.objects.filter(course_id=course_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LessonCreateSerializer
        return LessonSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['course_id'] = self.kwargs.get('course_id')
        return context
    
    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsLessonInstructorOrReadOnly]

class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

class EnrollmentCreateView(generics.CreateAPIView):
    serializer_class = EnrollmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsEnrollmentOwnerOrReadOnly]
    
    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

class ProgressUpdateView(generics.UpdateAPIView):
    serializer_class = ProgressUpdateSerializer
    permission_classes = [IsEnrollmentOwnerOrReadOnly]
    
    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

class CourseEnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        
        # Check if already enrolled
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response({
                'error': 'You are already enrolled in this course'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create enrollment
        enrollment = Enrollment.objects.create(user=request.user, course=course)
        serializer = EnrollmentSerializer(enrollment)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InstructorCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
