from rest_framework import serializers
from .models import Book
from comments.serializers import CommentSerializer


class BookSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    publication_date = serializers.DateField(
        format="%d/%m/%Y", input_formats=["%d/%m/%Y"]
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "genre",
            "publication_date",
            "description",
            "comments",
        )
