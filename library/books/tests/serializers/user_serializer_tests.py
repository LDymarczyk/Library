from rest_framework.test import APITestCase, APIRequestFactory
from ...models import Author, Book, Library, Reader, Rent
from ...serializers.user import UserSerializer
from rest_framework.exceptions import ValidationError, ErrorDetail
from datetime import datetime, date

def make_random_number():
    today = datetime.today()
    return str(today.hour) + str(today.min) + str(today.second) +str(today.microsecond)

class RentSerializersTests(APITestCase):

    def setUp(self):

        self.user_attrs = {'username': 'username',
                           'email': 'mail@mail.com',
                           'password': 'pass1234'}

        self.user = Reader.objects.create_user(**self.user_attrs)

        self.factory = APIRequestFactory()

    def test_contains_expected_fields_book_serializer(self):
        data = UserSerializer(instance=self.user)
        self.assertCountEqual(data.fields, {'username',
                                            'email',
                                            'password',
                                            'first_name',
                                            'last_name',
                                            'birth_date',
                                            'address',
                                            'telephone'
                                            })