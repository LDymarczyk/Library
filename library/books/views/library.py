from rest_framework import viewsets
from ..models.library import Library
from ..serializers.library import LibrarySerializer
from rest_framework import filters


class LibraryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('address', 'name')
    ordering_fields = ('address', 'name')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(editor=self.request.user, edited=datetime.today())
