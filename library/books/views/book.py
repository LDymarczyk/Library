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

    @action
    def show_avaible_books(self, request):


    @action(methods=['post'], detail=True)
    def rent_book(self, request, pk):
        #import pdb;pdb.set_trace()
        if Book.objects.filter(id=pk).status:
            user = Reader.objects.filter(id=request)
            return user
        else:
            raise ValueError('The book is already rented')

