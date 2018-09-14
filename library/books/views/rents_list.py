from ..models.rent import Rent
from ..serializers.rent import RentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RentList(APIView):

    def get(self, request, format=None):
        rent=Rent.objects.all()
        serializer = RentSerializer(rent, many = True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)