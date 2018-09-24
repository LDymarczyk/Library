from rest_framework import viewsets
from ..models.author import Author
from ..serializers.author import AuthorSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class AuthorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend,)
    search_fields = ('first_name', 'last_name', 'birth_year')
    ordering_fields = ('last_name', 'birth_date')
    filter_fields =('first_name', 'last_name', 'birth_year')

    def get_queryset(self):
        queryset = Author.objects.all()
        queryset = Author.add_fullname(queryset)
        fullname = self.request.query_params.get('fullname', None)
        if fullname: queryset = queryset.filter(fullname__icontains=fullname)
        return queryset


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


