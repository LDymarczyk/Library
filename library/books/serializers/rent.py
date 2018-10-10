from rest_framework import serializers
from ..models.rent import Rent
from ..models.book import Book
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class RentSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        # import pdb; pdb.set_trace()
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date>end_date:
            raise ValidationError("End date must be later than start date.")
        return attrs

    def validate_book(self, book):
        books = Book.objects.all()
        is_valid = False
        for volume in books:
            if volume == book:
                is_valid = True
        #import pdb; pdb.set_trace()
        if not is_valid:
            raise ValidationError("Book doesn't exist in base.")
        return book

    class Meta:
        model = Rent
        fields = ('start_date', 'end_date', 'book', 'reader', 'library')
        read_only_field = ('creator', 'id')