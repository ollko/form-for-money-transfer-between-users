from django.test import TestCase
from django.contrib.auth import get_user_model

from main.models import Profile

User = get_user_model()


class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'user', email="user@ya.ru", password="user")

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertTrue(isinstance(self.user.profile, Profile))
        self.assertEqual(self.user.profile.__str__(), 'user')
