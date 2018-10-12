from rest_framework import viewsets
from ..models import Reader, Rent
from ..serializers.user import UserSerializer
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

    @action(method=['get'], detail=True)
    def user_rent(self, request, pk=None):
        rents = Rent.objects.all()
        rents = [rent for rent in rents if rent.reader == pk]
        serializer = self.get_serializer_class()
        data = serializer(rents, many=True, context={request: 'request'}).data
        return Response(data)


