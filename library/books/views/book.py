from rest_framework import viewsets
from ..models.book import Book
from ..serializers.book import BookSerializer
from rest_framework import filters


class BookViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'author', 'ISBN', 'genre')
    ordering_fields = ('title', 'publication_date')


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

