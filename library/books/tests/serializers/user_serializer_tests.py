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
                                            'telephone',
                                            'PESEL'
                                            })

    def test_validate_with_correct_values(self):
        serializer = UserSerializer(instance=self.user, data=self.user_attrs)
        self.assertTrue(serializer.is_valid())

    def test_validate_with_short_PESEL(self):
        self.user_attrs['PESEL'] = 1111
        serializer = UserSerializer(instance=self.user, data=self.user_attrs)
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['PESEL'][0]
        self.assertEqual('PESEL number must have 11 digits.', error)
        self.assertFalse(serializer.is_valid())

    def test_validate_with_bad_PESEL(self):
        self.user_attrs['PESEL'] = 11111111111
        serializer = UserSerializer(instance=self.user, data=self.user_attrs)
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['PESEL'][0]
        self.assertEqual('PESEL number is incorrect.', error)
        self.assertFalse(serializer.is_valid())
