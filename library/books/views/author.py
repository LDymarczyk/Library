from rest_framework import viewsets
from ..models.author import Author
from ..serializers.author import AuthorSerializer
from django_filters import rest_framework as dfilters
from datetime import datetime


class AuthorFilter(dfilters.FilterSet):
    min_year = dfilters.NumberFilter(field_name="birth_year", lookup_expr='gte')
    max_year = dfilters.NumberFilter(field_name="birth_year", lookup_expr='lte')

    class Meta:
        model=Author
        fields = ['first_name', 'last_name', 'min_year', 'max_year']


class AuthorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (dfilters.DjangoFilterBackend,)
    filterset_class = AuthorFilter

    def get_queryset(self):
        queryset = Author.objects.all()
        queryset = Author.add_fullname(queryset)
        fullname = self.request.query_params.get('fullname', None)
        if fullname:
            queryset = queryset.filter(fullname__icontains=fullname)
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(editor=self.request.user, edited=datetime.today())



