from rest_framework import serializers
from .models import Comment
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "text", "owner", "username", "created_at", "updated_at")
        read_only_fields = ("owner", "created_at", "updated_at")

    def get_username(self, obj):
        return obj.owner.username
