from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Task


class TestTaskApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_one = get_user_model().objects.create_user("user_one@email.com", "1qazxsw2")
        self.user_two = get_user_model().objects.create_user("user_two@email.com", "1qazxsw2")

    def create_tasks_api(self, invalid=False):
        if not invalid:
            payload = {"title": "a task title", "description": "a task description"}
        else:
            payload = {"title": "", "description": ""}
        return self.client.post("/api/task/", payload)

    def create_tasks_db(self, user):
        defaults = {"title": "a task title", "description": "a task description"}
        return Task.objects.create(user=user, **defaults)

    def test_create_task(self):
        self.client.force_authenticate(self.user_one)
        response_one = self.create_tasks_api()
        response_two = self.create_tasks_api(invalid=True)
        self.assertEqual(response_one.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_two.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_user_tasks(self):
        self.client.force_authenticate(self.user_one)
        response = self.client.get("/api/task/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_with_owner(self):
        task_id = self.create_tasks_db(self.user_one).id
        self.client.force_authenticate(self.user_one)
        response = self.client.get(f"/api/task/{task_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_with_no_owner_user(self):
        task_id = self.create_tasks_db(self.user_two).id
        self.client.force_authenticate(self.user_one)
        response = self.client.get(f"/api/task/{task_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task_with_owner(self):
        task_id = self.create_tasks_db(self.user_one).id
        payload_one = {
            "title": "another task title",
            "description": "another task description",
            "completed": True,
        }

        payload_two = {"title": "", "description": "", "completed": True}
        self.client.force_authenticate(self.user_one)
        response_one = self.client.put(f"/api/task/{task_id}/", payload_one)
        response_two = self.client.put(f"/api/task/{task_id}/", payload_two)
        response_three = self.client.put("/api/task/1000/", payload_one)
        self.assertEqual(response_one.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("completed", response_one.data)
        self.assertEqual(response_two.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_three.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_with_no_owner_user(self):
        task_id = self.create_tasks_db(self.user_two).id
        payload = {
            "title": "another task title",
            "description": "another task description",
            "completed": True,
        }
        self.client.force_authenticate(self.user_one)
        response = self.client.put(f"/api/task/{task_id}/", payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task_with_owner(self):
        task_id = self.create_tasks_db(self.user_one).id
        self.client.force_authenticate(self.user_one)
        response_one = self.client.delete(f"/api/task/{task_id}/")
        response_two = self.client.delete(f"/api/task/1000/")
        self.assertEqual(response_one.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn("message", response_one.data)
        self.assertEqual(response_two.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task_with_no_owner(self):
        task_id = self.create_tasks_db(self.user_two).id
        self.client.force_authenticate(self.user_one)
        response = self.client.delete(f"/api/task/{task_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_not_exist_object(self):
        self.client.force_authenticate(self.user_one)
        response = self.client.get("/api/task/1000/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
