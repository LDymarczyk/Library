from rest_framework.test import APITestCase, APIRequestFactory
from ...models import Author, Book, Rent, Library, Reader
from ...serializers.author import AuthorSerializer

class AuthorSerializersTests(APITestCase):

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

        # self.library = Library.objects.create(address='ul. Klonowa 2, 40-000 Katowice',
        #                                       email='bibl@mail.com',
        #                                       name='Biblioteka 1',
        #                                       telephone=123456789)
        #
        # self.book = Book.objects.create(title='title1',
        #                                 author=self.author,
        #                                 ISBN=1234567890123,
        #                                 genre='FS',
        #                                 edition=1,
        #                                 publication_date=2005,
        #                                 publishing_house='FS',
        #                                 status=True,
        #                                 library=self.library
        #                                 )

        self.factory = APIRequestFactory()

    def test_contains_expected_fields_author_serializer(self):
        data = AuthorSerializer(instance=self.author)
        self.assertCountEqual(data.fields, {'first_name', 'last_name',
                                            'birth_year', 'death_year'})

    def test_validate_with_valid_author(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Kowalski',
                'birth_year' : 1990, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        self.assertTrue(serializer.is_valid())

    def test_validate_author_serializer_with_bad_first_name(self):
        data = {'first_name' : 'A', 'last_name' : 'Kowalski',
                'birth_year' : 1990, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_with_bad_last_name(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Ko',
                'birth_year' : 1990, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_with_bad_birth_year(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Kowalski',
                'birth_year' : 1000, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_with_bad_birth_death_year(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Kowalski',
                'birth_year' : 1900, 'death_year' : 1800}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        self.assertFalse(serializer.is_valid())



