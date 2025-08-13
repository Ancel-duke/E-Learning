from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test that user profile is automatically created when user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user_type, 'student')
    
    def test_user_profile_properties(self):
        """Test user profile properties"""
        self.assertTrue(self.user.profile.is_student)
        self.assertFalse(self.user.profile.is_instructor)
        
        # Change to instructor
        self.user.profile.user_type = 'instructor'
        self.user.profile.save()
        
        self.assertTrue(self.user.profile.is_instructor)
        self.assertFalse(self.user.profile.is_student)

class AccountsAPITest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.change_password_url = reverse('change_password')
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'student'
        }
    
    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        
        user = User.objects.first()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.profile.user_type, 'student')
    
    def test_user_registration_password_mismatch(self):
        """Test user registration with password mismatch"""
        self.user_data['password2'] = 'wrongpassword'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login(self):
        """Test user login"""
        # Create user first
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
    
    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials"""
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_profile_retrieve(self):
        """Test retrieving user profile"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_user_profile_update(self):
        """Test updating user profile"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.patch(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
    
    def test_change_password(self):
        """Test changing user password"""
        user = User.objects.create_user(
            username='testuser',
            password='oldpassword'
        )
        self.client.force_authenticate(user=user)
        
        password_data = {
            'old_password': 'oldpassword',
            'new_password': 'newpassword123',
            'new_password2': 'newpassword123'
        }
        
        response = self.client.put(self.change_password_url, password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test login with new password
        self.client.logout()
        login_data = {
            'username': 'testuser',
            'password': 'newpassword123'
        }
        login_response = self.client.post(self.login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
    
    def test_change_password_wrong_old_password(self):
        """Test changing password with wrong old password"""
        user = User.objects.create_user(
            username='testuser',
            password='oldpassword'
        )
        self.client.force_authenticate(user=user)
        
        password_data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123',
            'new_password2': 'newpassword123'
        }
        
        response = self.client.put(self.change_password_url, password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
