from django.contrib.auth import get_user_model
from django.test import TestCase


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


class UserModelsTests(TestCase):
    def test_create_user_with_empty_email(self):
        payload = {"email": "", "password": "1qazxsw2", "name": "User name"}
        with self.assertRaises(ValueError):
            create_user(**payload)

    def test_create_valid_superuser(self):
        payload = {"email": "admin@email.com", "password": "1qazxsw2"}
        superuser = create_superuser(**payload)
        self.assertIsInstance(superuser.email, str)

    def test_create_superuser_with_empty_email(self):
        payload = {"email": "", "password": "1qazxsw2"}
        with self.assertRaises(ValueError):
            create_superuser(**payload)
