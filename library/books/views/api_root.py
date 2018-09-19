from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'authors': reverse('authors-list', request=request, format=format),
        'books': reverse('books-list', request=request, format=format),
        'libraries': reverse('libraries-list', request=request, format=format),
        'rents': reverse('rents-list', request=request, format=format),
        'users': reverse('users-list', request=request, format=format),
    })