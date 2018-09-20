from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from ..models.author import Author
from ..serializers.author import AuthorSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
    #permission_classes = (IsAuthenticatedOrReadOnly,)

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


