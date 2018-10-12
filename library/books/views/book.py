from rest_framework import viewsets
from ..models import Book, Rent
from ..serializers.book import BookSerializer
from ..serializers.rent import RentSerializer
from rest_framework import filters
from django_filters import rest_framework as dfilters
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime


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

    def perform_update(self, serializer):
        serializer.save(editor=self.request.user, edited=datetime.today())

    @action(methods=['get'], detail=False)
    def show_available_books(self, request):
        books = Book.objects.all()
        books = [book for book in books if book.status]
        serializer = self.get_serializer_class()
        data = serializer(books, many=True, context={"request": request}).data
        return Response(data)

    @action(methods=['get'], detail=True)
    def history(self, request, pk=None):
        rents = Rent.objects.all()
        #import pdb; pdb.set_trace()
        rents = [rent for rent in rents if str(rent.book.pk) == pk]
        serializer = RentSerializer
        data = serializer(rents, many=True, context={"request": request}).data
        return Response(data)


