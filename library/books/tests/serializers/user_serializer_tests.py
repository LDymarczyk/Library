from rest_framework.test import APITestCase, APIRequestFactory
from ...models import Reader
from ...serializers.user import UserSerializer
from rest_framework.exceptions import ValidationError, ErrorDetail
from datetime import datetime, date

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

    def test_validate_with_correct_values(self):
        serializer = UserSerializer(instance=self.user, data=self.user_attrs)
        self.assertTrue(serializer.is_valid())

    # def test_validate_with_non_existing_book(self):
    #     self.rent_attrs['book'] = self.book.pk + 500000
    #     serializer = RentSerializer(instance=self.rent, data=self.rent_attrs)
    #     with self.assertRaises(ValidationError) as cm:
    #         serializer.is_valid(raise_exception=True)
    #     error = cm.exception.args[0]['book'][0]
    #     self.assertEqual(ErrorDetail(string='Invalid pk "' + str(self.book.pk + 500000) + '" - object does not exist.', code='does_not_exist'), error)
    #     self.assertFalse(serializer.is_valid())