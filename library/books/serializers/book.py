from rest_framework import serializers
from ..models.book import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'ISBN', 'genre', 'edition', 'amount', 'publication_date', 'publishing_house',
                  'language', 'status', 'library')