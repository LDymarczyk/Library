from ..models.author import Author
from ..serializers.author import AuthorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets


class AuthorList(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    # search_fields = ('first_name', 'last_name')

    # def get_queryset(self):
    #     return self.queryset

    # def get(self, request, format=None):
    #     author=Author.objects.all()
    #     serializer = AuthorSerializer(author, many = True)
    #     return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     serializer = AuthorSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


# class AuthorListF(generics.ListAPIView):
#     queryset = Author.objects.all()
#     serializer = AuthorSerializer
#     filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
#     search_fields = ('first_name', 'last_name')

