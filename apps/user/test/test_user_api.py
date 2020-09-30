from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

USER_CREATION_URL = reverse("user:create")
USER_TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        payload = {"email": "email@email.com", "password": "1qazxsw2", "name": "User name"}
        response = self.client.post(USER_CREATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_create_existing_user(self):
        payload = {"email": "email@email.com", "password": "1qazxsw2"}
        create_user(**payload)
        response = self.client.post(USER_CREATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {"email": "email@email.com", "password": "ps"}
        response = self.client.post(USER_CREATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        payload = {"email": "email@email.com", "password": "1qazxsw2"}
        create_user(**payload)
        response = self.client.post(USER_TOKEN_URL, payload)

        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(email="email@email.com", password="1qazxsw2")
        payload = {"email": "email@email.com", "password": "wrongpass"}
        response = self.client.post(USER_TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
