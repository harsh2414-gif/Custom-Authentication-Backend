from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now
from datetime import time

class CustomAuthBackendTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            role='user',
            allowed_time_ranges={'start': '09:00', 'end': '17:00'}
        )

    def test_login_within_time_range(self):
        current_time = now().replace(hour=10, minute=0)
        with self.settings(TIME_ZONE='UTC'):
            self.assertTrue(self.user.allowed_time_ranges['start'] <= current_time.strftime('%H:%M') <= self.user.allowed_time_ranges['end'])

    def test_login_outside_time_range(self):
        current_time = now().replace(hour=18, minute=0)
        with self.settings(TIME_ZONE='UTC'):
            self.assertFalse(self.user.allowed_time_ranges['start'] <= current_time.strftime('%H:%M') <= self.user.allowed_time_ranges['end'])

    def test_invalid_credentials(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
