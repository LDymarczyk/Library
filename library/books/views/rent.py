from rest_framework import viewsets
from ..models.rent import Rent
from ..serializers.rent import RentSerializer
from rest_framework import filters


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
        serializer.save(creator=self.request.user)

