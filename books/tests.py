from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book
from services.models import CustomUser


class BookTests(APITestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass"
        )

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        self.book = Book.objects.create(
            title="Test Book",
            author="Author Test",
            genre="Genre Test",
            publication_date="2020-01-01",
            description="Test description",
        )

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_list_books(self):
        self.authenticate()
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book(self):
        self.authenticate()
        url = reverse("book_list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "genre": "New Genre",
            "publication_date": "24/07/2024",
            "description": "New description",
        }
        response = self.client.post(url, data, format="json")

        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_book(self):
        self.authenticate()
        url = reverse("book_detail", args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_update_book(self):
        self.authenticate()
        url = reverse("book_detail", args=[self.book.id])
        data = {
            "title": "Updated Book",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        self.authenticate()
        url = reverse("book_detail", args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_token_obtain_pair(self):
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        url = reverse("token_refresh")
        data = {"refresh": str(self.refresh)}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
