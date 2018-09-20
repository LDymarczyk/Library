from ..models.author import Author
from ..serializers.author import AuthorSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
import django_filters.rest_framework


class AuthorFilter(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_queryset(self):
        queryset=Author.objects.all()
        first_name=self.request.query_params.get('first_name', None)
        if first_name is not None:
            queryset = queryset.filter(author__first_name=first_name)
        return queryset