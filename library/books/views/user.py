from rest_framework import viewsets
from ..models import Reader, Rent
from ..serializers.user import UserSerializer
from ..serializers.rent import RentSerializer
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Reader.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('PESEL', 'first_name', 'last_name')
    ordering_fields = ('first_name', 'last_name')

    @action(methods=['get'], detail=True)
    def user_rents(self, request, pk=None):
        rents = Rent.objects.all()
        rents = [rent for rent in rents if str(rent.reader.pk) == pk]
        serializer = RentSerializer
        data = serializer(rents, many=True, context={request: 'request'}).data
        return Response(data)

    @action(methods=['get'], detail=True)
    def currently_rented(self, request, pk=None):
        rents = Rent.objects.all()
        rents = [rent for rent in rents if str(rent.reader.pk) == pk and rent.status]
        serializer = RentSerializer
        data = serializer(rents, many=True, context={request: 'request'}).data
        return Response(data)
