from rest_framework import serializers
from .models import Course, Lesson, Enrollment
from accounts.serializers import UserSerializer

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'materials', 'order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    total_lessons = serializers.ReadOnlyField()
    total_enrollments = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'category', 'difficulty', 
            'instructor', 'thumbnail', 'created_at', 'updated_at',
            'lessons', 'total_lessons', 'total_enrollments'
        ]
        read_only_fields = ['created_at', 'updated_at', 'instructor']

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'difficulty', 'thumbnail']
    
    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)

class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'materials', 'order']
    
    def validate_order(self, value):
        course_id = self.context.get('course_id')
        if course_id:
            existing_lesson = Lesson.objects.filter(course_id=course_id, order=value).exists()
            if existing_lesson:
                raise serializers.ValidationError("A lesson with this order already exists in this course.")
        return value

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'user', 'enrollment_date', 'progress', 'completed']
        read_only_fields = ['enrollment_date', 'user']

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['course']
    
    def validate_course(self, value):
        user = self.context['request'].user
        if Enrollment.objects.filter(user=user, course=value).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ProgressUpdateSerializer(serializers.Serializer):
    progress = serializers.IntegerField(min_value=0, max_value=100)
    
    def update(self, instance, validated_data):
        instance.update_progress(validated_data['progress'])
        return instance
