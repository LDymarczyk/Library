from rest_framework.test import APITestCase, APIRequestFactory
from ...models import Author, Book, Rent, Library, Reader
from ...serializers.author import AuthorSerializer
from ...serializers.book import BookSerializer
from rest_framework.exceptions import ValidationError

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

        self.library = Library.objects.create(address='ul. Klonowa 2, 40-000 Katowice',
                                              email='bibl@mail.com',
                                              name='Biblioteka 1',
                                              phone='123456789')

        self.book = Book.objects.create(title='title1',
                                        author=self.author,
                                        ISBN=1234567890123,
                                        genre='FS',
                                        edition=1,
                                        publication_date=2005,
                                        publishing_house='FS',
                                        status=True,
                                        library=self.library
                                        )

        def test_contains_expected_fields_book_serializer(self):
            data = AuthorSerializer(instance=self.book)
            self.assertCountEqual(data.fields, {'title',
                                                'author',
                                                'ISBN',
                                                'genre',
                                                'edition',
                                                'publication_date',
                                                'publishing_house',
                                                'status',
                                                'library'
                                                })