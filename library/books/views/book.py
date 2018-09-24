from rest_framework import viewsets
from ..models.book import Book
from ..serializers.book import BookSerializer
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status


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
        serializer.save(creator=self.request.user)
    #
    # def create(self, request, *args, **kwargs):
    #     serializer = BookSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(creator=self.request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

