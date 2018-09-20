from rest_framework import viewsets
from ..models.user import Reader
from ..serializers.user import UserSerializer
from rest_framework import filters


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


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

