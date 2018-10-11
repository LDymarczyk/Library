from rest_framework.test import APITestCase, APIRequestFactory
from ...models import Author, Book, Library, Reader
from ...serializers.book import BookSerializer
from rest_framework.exceptions import ValidationError, ErrorDetail
from datetime import datetime

class BookSerializersTests(APITestCase):

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

        today = datetime.today()
        number = str(today.hour)+str(today.min)+str(today.second)

        self.library = Library.objects.create(address='ul. Klonowa 2, 40-000 Katowice',
                                              email='bibl@mail.com',
                                              name='Biblioteka '+number,
                                              phone='123456789')

        self.book = Book.objects.create(title='title1',
                                        author=self.author,
                                        ISBN=1234567890123,
                                        genre='FS',
                                        edition=1,
                                        amount=12,
                                        publication_date=2005,
                                        publishing_house='FS',
                                        status=True,
                                        library=self.library
                                        )

        self.factory = APIRequestFactory()

    def test_contains_expected_fields_book_serializer(self):
        data = BookSerializer(instance=self.book)
        self.assertCountEqual(data.fields, {'title',
                                            'author',
                                            'ISBN',
                                            'genre',
                                            'edition',
                                            'amount',
                                            'language',
                                            'creator',
                                            'publication_date',
                                            'publishing_house',
                                            'status',
                                            'library',
                                            'id',
                                            'editor',
                                            'edited',
                                            'created'})

    def test_validate_with_correct_values(self):
        author = self.author
        user = self.user
        data = {'title':'T',
                'author': author.pk,
                'creator': user.pk,
                'ISBN':1234567890123,
                'genre':'FS',
                'edition':1,
                'amount':2,
                'language':'polski',
                'publication_date':1500,
                'publishing_house':'Fabryka Słów',
                'status':True}
        request = self.factory.get('/')
        request.user = self.user
        serializer = BookSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_validate_with_bad_author(self):
        user = self.user
        data = {'title': 'T',
                'author': 1000,
                'creator': user.pk,
                'ISBN': 1234567890123,
                'genre': 'FS',
                'edition': 1,
                'amount': 2,
                'language': 'polski',
                'publication_date': 1500,
                'publishing_house': 'Fabryka Słów',
                'status': True}
        request = self.factory.get('/')
        request.user = self.user
        serializer = BookSerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['author'][0]
        self.assertEqual('does_not_exist', error.code)
        self.assertFalse(serializer.is_valid())

    def test_validate_with_bad_ISBN(self):
        author = self.author
        user = self.user
        data = {'title': 'T',
                'author': author.pk,
                'creator': user.pk,
                'ISBN': 5,
                'genre': 'FS',
                'edition': 1,
                'amount': 2,
                'language': 'polski',
                'publication_date': 1500,
                'publishing_house': 'Fabryka Słów',
                'status': True}
        request = self.factory.get('/')
        request.user = self.user
        serializer = BookSerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['ISBN'][0]
        self.assertEqual('ISBN number must have exactly 10 or 13 digits.', error)
        self.assertFalse(serializer.is_valid())

    def test_validate_with_bad_genre(self):
        author = self.author
        user = self.user
        data = {'title': 'T',
                'author': author.pk,
                'creator': user.pk,
                'ISBN': 1234567890123,
                'genre': 'AAA',
                'edition': 1,
                'amount': 2,
                'language': 'polski',
                'publication_date': 1500,
                'publishing_house': 'Fabryka Słów',
                'status': True}
        request = self.factory.get('/')
        request.user = self.user
        serializer = BookSerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['genre'][0]
        self.assertEqual('invalid_choice', error.code)
        self.assertFalse(serializer.is_valid())

    def test_validate_with_bad_publication_date(self):
        author = self.author
        user = self.user
        data = {'title': 'T',
                'author': author.pk,
                'creator': user.pk,
                'ISBN': 1234567890123,
                'genre': 'FS',
                'edition': 1,
                'amount': 2,
                'language': 'polski',
                'publication_date': 1000,
                'publishing_house': 'Fabryka Słów',
                'status': True}
        request = self.factory.get('/')
        request.user = self.user
        serializer = BookSerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['publication_date'][0]
        self.assertEqual('Publication date must be greater than 1450. Printing was invented in 1450.', error)
        self.assertFalse(serializer.is_valid())

    def test_validate_with_bad_status(self):
        author = self.author
        user = self.user
        data = {'title':'T',
                'author': author.pk,
                'creator': user.pk,
                'ISBN':1234567890123,
                'genre':'FS',
                'edition':1,
                'amount':0,
                'language':'polski',
                'publication_date':1500,
                'publishing_house':'Fabryka Słów',
                'status':True}
        request = self.factory.get('/')
        request.user = self.user
        serializer = BookSerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['non_field_errors'][0]
        self.assertEqual("Status of book can't be True if there are no books.", error)
        self.assertFalse(serializer.is_valid())

    def test_validate_with_bad_publication_date_future(self):
        author = self.author
        user = self.user
        data = {'title':'T',
                'author': author.pk,
                'creator': user.pk,
                'ISBN':1234567890123,
                'genre':'FS',
                'edition':1,
                'amount':2,
                'language':'polski',
                'publication_date':500000,
                'publishing_house':'Fabryka Słów',
                'status':True}
        request = self.factory.get('/')
        request.user = self.user
        serializer = BookSerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['publication_date'][0]
        self.assertEqual("This book will be publish in the future.", error)
        self.assertFalse(serializer.is_valid())



