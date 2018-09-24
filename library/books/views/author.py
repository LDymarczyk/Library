from rest_framework import viewsets
from ..models.author import Author
from ..serializers.author import AuthorSerializer
from rest_framework import filters


class AuthorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('first_name', 'last_name')
    ordering_fields = ('last_name', 'birth_date')


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


