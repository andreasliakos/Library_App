from django.db import models
from services.models import CustomUser
from books.models import Book


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    owner = models.ForeignKey(
        CustomUser, related_name="comments", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.owner.username} on {self.book.title}"


# dhbchj
