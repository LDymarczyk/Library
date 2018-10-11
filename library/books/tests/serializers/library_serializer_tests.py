from rest_framework.test import APITestCase, APIRequestFactory
from ...models import Author, Book, Library, Reader
from ...serializers.library import LibrarySerializer
from rest_framework.exceptions import ValidationError, ErrorDetail
from datetime import datetime
from ..tools import make_random_number

class LibrarySerializersTests(APITestCase):

    def setUp(self):

        self.user = Reader.objects.create_user(username='Ala',
                                               email='mail@mail.com',
                                               password='pass')

        self.author = Author.objects.create(first_name='Jan',
                                            last_name='Kowalski',
                                            birth_year=1990,
                                            death_year=2017,
                                            creator=self.user)

        self.author2 = Author.objects.create(first_name='Ala',
                                             last_name='MaKota',
                                             birth_year=1890,
                                             death_year=1917,
                                             creator=self.user)

        self.library = Library.objects.create(address='ul. Klonowa 2, 40-000 Katowice',
                                              email='bibl@mail.com',
                                              name='Biblioteka ' + make_random_number(),
                                              phone='123456789')


        self.factory = APIRequestFactory()

    def test_contains_expected_fields_book_serializer(self):
        data = LibrarySerializer(instance=self.library)
        self.assertCountEqual(data.fields, {'address',
                                            'email',
                                            'name',
                                            'phone',
                                            'id',
                                            'creator',
                                            'editor',
                                            'created',
                                            'edited'
                                            })

    def test_validate_with_correct_values(self):
        data = {'address':"aaaaaaa",
                'email':"email@email.com",
                'name':"aaaaaaa"+make_random_number(),
                'phone':"123456789"}
        request = self.factory.get('/')
        request.user = self.user
        serializer = LibrarySerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_validate_with_bad_email(self):
        data = {'address':"aaaaaaa",
                'email':"email",
                'name':"aaaaaaa"+make_random_number(),
                'phone':"123456789"}
        request = self.factory.get('/')
        request.user = self.user
        serializer = LibrarySerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['email'][0]
        self.assertEqual(ErrorDetail(string='Enter a valid email address.', code='invalid'), error)
        self.assertFalse(serializer.is_valid())

    def test_validate_with_bad_phone(self):
        data = {'address':"aaaaaaa",
                'email':"email@email.com",
                'name':"aaaaaaa"+make_random_number(),
                'phone':"12"}
        request = self.factory.get('/')
        request.user = self.user
        serializer = LibrarySerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['phone'][0]
        self.assertEqual("Entered bad phone number.", error)
        self.assertFalse(serializer.is_valid())