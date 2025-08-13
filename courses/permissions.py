from rest_framework import permissions

class IsInstructorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow instructors to create/edit courses.
    Students can view courses.
    """
    
    def has_permission(self, request, view):
        # Allow read operations for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is authenticated and is an instructor
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_instructor

class IsCourseInstructorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow course instructor to edit the course.
    Others can view the course.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow read operations for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is the instructor of the course
        return obj.instructor == request.user

class IsLessonInstructorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow course instructor to edit lessons.
    Others can view lessons.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow read operations for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is the instructor of the course
        return obj.course.instructor == request.user

class IsEnrollmentOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow enrollment owner to update their enrollment.
    Others can view enrollments.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow read operations for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is the owner of the enrollment
        return obj.user == request.user
