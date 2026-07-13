from django.contrib.auth.models import User
from django.test import TestCase


class RedirectNamespaceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice@example.com',
            email='alice@example.com',
            password='secret123',
        )

    def test_authenticated_user_welcome_redirects_to_home(self):
        self.client.login(username='alice@example.com', password='secret123')

        response = self.client.get('/welcome/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home/')
