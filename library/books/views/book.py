from rest_framework import viewsets
from ..models.book import Book
from ..models.library import Library
from ..models.user import Reader
from ..models.rent import Rent
from ..serializers.book import BookSerializer
from ..serializers.rent import RentSerializer
from rest_framework import filters
from django_filters import rest_framework as dfilters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date, timedelta


class BookFilter(dfilters.FilterSet):
    min_year = dfilters.NumberFilter(field_name="publication_date", lookup_expr='gte')
    max_year = dfilters.NumberFilter(field_name="publication_date", lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['min_year', 'max_year', 'author', 'genre', 'publishing_house','ISBN']


class BookViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (dfilters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('title', 'publication_date')
    filterset_class = BookFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(methods=['get'], detail=False)
    def show_avaible_books(self, request):
        books = list(Book.objects.all())
        books = [book for book in books if book.status]
        serializer = self.get_serializer_class()
        data = serializer(books, many=True, context={"request": request}).data
        return Response(data)

    @action(methods=['post'], detail=True)
    def rent_book(self, request, pk):
        import pdb;pdb.set_trace()
        book = get_object_or_404(Book, pk=pk)
        if book.status:
            data = request.data
            user_pk = data['user']
            user = Reader.objects.get(id=user_pk)
            today = date.today() + timedelta(days = 7)
            Rent.objects.create(reader=user, book=book, end_date=today)
        else:
            raise ValueError('The book is already rented')

