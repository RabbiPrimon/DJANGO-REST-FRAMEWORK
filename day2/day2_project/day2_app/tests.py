from rest_framework import status
from rest_framework.test import APITestCase

from .models import Todo


class TodoApiTests(APITestCase):
    def setUp(self):
        self.pending = Todo.objects.create(
            title="Learn DRF",
            is_done=False,
        )
        self.done = Todo.objects.create(
            title="Setup project",
            is_done=True,
        )

    def test_create_todo(self):
        payload = {
            "title": "Write tests",
            "is_done": False,
        }

        response = self.client.post("/todos/create/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 3)
        self.assertEqual(Todo.objects.get(title="Write tests").is_done, False)

    def test_todo_list_returns_all_todos(self):
        response = self.client.get("/todos/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.pending.id)

    def test_done_todo_list_returns_only_done_todos(self):
        response = self.client.get("/done-todos/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.done.id)
