from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .models import Comment, Book
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .serializers import CommentSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


ensure_csrf_cookie_decorator = method_decorator(ensure_csrf_cookie)
user = get_user_model()


class CommentCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        return Comment.objects.filter(book_id=book_id, owner=self.request.user)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        book_id = self.kwargs.get("book_id")
        book = generics.get_object_or_404(Book, pk=book_id)
        owner = self.request.user
        serializer.save(book=book, owner=owner)


class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(ensure_csrf_cookie)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        comment_id = self.kwargs.get("pk")
        return Comment.objects.filter(pk=comment_id, owner=self.request.user)
