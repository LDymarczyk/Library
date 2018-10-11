from rest_framework import viewsets
from ..models.rent import Rent
from ..models.book import Book
from ..serializers.rent import RentSerializer
from rest_framework import filters, status
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta
from rest_framework.response import Response
from django.http import Http404
from rest_framework.decorators import action


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
            start_date = datetime.strptime(self.request.data['start_date'], '%Y-%m-%d').date()
        if 'end_date' not in self.request.data.keys():
            end_date = start_date + timedelta(days=14)
        else:
            end_date = self.request.data['end_date']
        book.rent_book()
        serializer.save(creator=self.request.user, end_date=end_date, start_date=start_date)

    def perform_update(self, serializer):
        serializer.save(editor=self.request.user, edited=datetime.today())

    def destroy(self, request, *args, **kwargs):
        #import pdb; pdb.set_trace()
        try:
            instance = self.get_object()
            instance.return_book()
            instance.save()
            instance.get_book().return_book()
            instance.get_book().save()
            #self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):

        pass

    @action(methods=['delete'], detail=True)
    def regulate_payment(self, request, pk=None):
        import pdb; pdb.set_trace()
        instance = self.get_object()
        if instance.late and not instance.regulated_payment:
            instance.cost = 0
            instance.regulated_payment = True
            instance.status = False
        pass

