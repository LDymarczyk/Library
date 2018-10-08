from rest_framework.test import APITestCase, APIRequestFactory
from ...models import Author, Book, Library, Reader
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
                                            'library'})

    def test_validate_with_existing_author(self):
        author = self.author
        user = self.user
        data = {'title':'T',
                'author': author,
                'creator': user,
                'ISBN':1234567890123,
                'genre':'Fantasy',
                'edition':1,
                'amount':2,
                'language':'polski',
                'publication_date':1300,
                'publishing_house':'Fabryka Słów',
                'status':True}
        request = self.factory.get('/')
        request.user = self.user
        serializer = BookSerializer(data=data, context={'request': request})
        #import pdb; pdb.set_trace()
        self.assertTrue(serializer.is_valid())

    # def test_validate_with_fake_author(self):
    #
    # def test_validate_with_bad_ISBN(self):
    #
    # def test_valdate_with_correct_ISBN(self):

