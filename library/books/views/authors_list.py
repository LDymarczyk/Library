from ..models.author import Author
from ..serializers.author import AuthorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AuthorList(APIView):

    def get(self, request, format=None):
        author=Author.objects.all()
        serializer = AuthorSerializer(author, many = True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AuthorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)