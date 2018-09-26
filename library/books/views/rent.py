from rest_framework import viewsets
from ..models.rent import Rent
from ..models.book import Book
from ..serializers.rent import RentSerializer
from rest_framework import filters
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta


class RentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('book', 'reader', 'rent_id')
    ordering_fields = ('rent_id', 'book')

    def perform_create(self, serializer):
        #import pdb; pdb.set_trace()
        book_id = self.request.data['book']
        book = get_object_or_404(Book, pk=book_id)
        if not book.status:
            raise ValidationError("book is already rented")
        if 'start_date' not in self.request.data.keys():
            start_date = date.today()
        else:
            start_date = datetime.strptime(self.request.data['start_date'],'%Y-%m-%d').date()
        if 'end_date' not in self.request.data.keys():
            end_date = start_date + timedelta(days=14)
        else:
            end_date = self.request.data['end_date']
        book.amount -= 1
        serializer.save(creator=self.request.user, end_date=end_date, start_date=start_date)



