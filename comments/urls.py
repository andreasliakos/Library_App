from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CommentCreate,
    CommentDelete,
)


urlpatterns = [
    path(
        "books/<int:book_id>/comments/", CommentCreate.as_view(), name="comment_create"
    ),
    path("comments/<int:pk>/", CommentDelete.as_view(), name="comment-delete"),
]
