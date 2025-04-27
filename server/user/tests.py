from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.registration_url = reverse('register')

    def test_valid_registration(self):
        """
        Test successful user registration with valid data.
        """
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)  # Verify user was created
        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

    def test_missing_username(self):
        """
        Test registration with missing username.
        """
        data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)  # Check for the error message

    def test_missing_password(self):
        """
        Test registration with missing password.
        """
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_invalid_email(self):
        """
        Test registration with an invalid email address.
        """
        data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_duplicate_username(self):
        """
        Test registration with a duplicate username.
        """
        # Create a user first
        User.objects.create_user(
            username="existinguser", email="existing@example.com", password="password"
        )
        data = {
            "username": "existinguser",
            "email": "newuser@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_duplicate_email(self):
        """
        Test registration with a duplicate email.
        """
        # Create a user first
        User.objects.create_user(
            username="existinguser", email="existing@example.com", password="password"
        )
        data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


class UserLoginTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )
        self.login_url = reverse('login')

    def test_login_success(self):
        """
        Test successful login with correct credentials.
        """
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    def test_login_failure_invalid_credentials(self):
        """
        Test login with incorrect password.
        """
        data = {
            "username": "testuser",
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials")

    def test_login_failure_missing_username(self):
        """
        Test login with missing username.
        """
        data = {
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"],
            "Please provide username and password"
        )

    def test_login_failure_missing_password(self):
        """
        Test login with missing password.
        """
        data = {
            "username": "testuser",
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"],
            "Please provide username and password"
        )

    def test_login_failure_invalid_username(self):
        """
        Test login with invalid username.
        """
        data = {
            "username": "nonexistentuser",
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials")


class UserInfoTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        # Create a token for the test user
        self.token = Token.objects.create(user=self.user)
        # Set up default authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        # Get URL for the /api/user/me/ endpoint
        self.user_me_url = reverse('user_info')

    def test_get_user_info_authenticated(self):
        """
        Test getting user info with a valid token.
        """
        response = self.client.get(self.user_me_url)
        expected_data = UserSerializer(self.user).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_user_info_unauthenticated(self):
        """
        Test getting user info without a token.
        """
        self.client.credentials()  # Clear the default authentication
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
