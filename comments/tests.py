from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from services.models import CustomUser
from books.models import Book
from comments.models import Comment


class CommentAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            genre="Fiction",
            publication_date="2023-01-01",
            description="blah blah blah",
        )
        self.comment = Comment.objects.create(
            book=self.book, text="Test Comment", owner=self.user
        )

        self.client.login(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_create_comment(self):
        url = reverse("comment_create", kwargs={"book_id": self.book.id})
        data = {"text": "New Comment"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.latest("created_at").text, "New Comment")

    def test_delete_comment(self):
        url = reverse("comment-delete", kwargs={"pk": self.comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_retrieve_comments_for_book(self):
        url = reverse("comment_create", kwargs={"book_id": self.book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["text"], "Test Comment")

    def test_create_comment_unauthenticated(self):
        self.client.logout()
        url = reverse("comment_create", kwargs={"book_id": self.book.id})
        data = {"text": "New Comment"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_unauthenticated(self):
        self.client.logout()
        url = reverse("comment-delete", kwargs={"pk": self.comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
