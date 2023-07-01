from rest_framework import serializers
from book.models.book import Book
from book.models.page import Page


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()

    class Meta:
        model = Page
        fields = ["id", "page_number", "content", "book"]
