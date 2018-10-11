from rest_framework.test import APIClient, APITestCase
from rest_framework.renderers import JSONRenderer
from ...models import Author, Reader, Book
from ...serializers.book import BookSerializer


class BookPermissionTest(APITestCase):

    def setUp(self):
        self.superuser = Reader.objects.create_superuser(username='useradmin',
                                                         email='useradmin@mail.com',
                                                         password='pass1234')

        self.user = Reader.objects.create_user(username='alamakota',
                                               first_name="Ala",
                                               last_name="MaKota",
                                               email='email@email.com',
                                               password='pass1234',
                                               PESEL=12344678901)

        self.user2 = Reader.objects.create_user(username='alaniemakota',
                                                first_name="Ala",
                                                last_name="NieMaKota",
                                                email='email@email.com',
                                                password='pass1234',
                                                PESEL=12344678901)

        self.author_attrs = {'first_name': 'Adam',
                             'last_name': 'Kowalski',
                             'birth_year': 1800,
                             'death_year': 1850}

        self.author = Author.objects.create(**self.author_attrs)

        self.book_attrs = {'title': 'Tytuł tom 1',
                           'author': self.author,
                           'ISBN': 1234567890123,
                           'genre': 'FS',
                           'edition': 1,
                           'amount': 2,
                           'language': 'polski',
                           'publication_date': 1900,
                           'publishing_house': 'FS',
                           'status': True}

        self.book_attrs2 = {'title': 'Tytuł tom 5',
                            'author': self.author,
                            'ISBN': 1234567890123,
                            'genre': 'FS',
                            'edition': 3,
                            'amount': 2,
                            'language': 'polski',
                            'publication_date': 1900,
                            'publishing_house': 'FS',
                            'status': False}

        self.book_attrs3 = {'title': 'Tytuł tom 6',
                            'author': self.author,
                            'ISBN': 1234567890123,
                            'genre': 'FS',
                            'edition': 3,
                            'amount': 2,
                            'language': 'polski',
                            'publication_date': 1900,
                            'publishing_house': 'FS',
                            'status': True}

        self.book = Book.objects.create(**self.book_attrs)
        self.book2 = Book.objects.create(**self.book_attrs2)
        self.book3 = Book.objects.create(**self.book_attrs3)

        self.book_list_url = '/books/'
        self.book_detail_url = '/books/{}/'.format(self.book.pk)
        self.book_available_action_url = '/books/show_available_books/'

    def test_book_perform_create_method(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        self.book_attrs['author'] = self.author.pk
        response_create_book = client.post(self.book_list_url, self.book_attrs, format='json')
        self.assertEqual(response_create_book.status_code, 201)
        self.assertTrue(Book.objects.filter(title='Tytuł tom 1', creator=self.superuser).exists())

    def test_book_perform_create_method_with_anonymous(self):
        client = APIClient()
        self.book_attrs['author'] = self.author.pk
        self.book_attrs['title'] = 'test title'
        response_create_book = client.post(self.book_list_url, self.book_attrs, format='json')
        self.assertEqual(response_create_book.status_code, 403)
        self.assertFalse(Book.objects.filter(title='test title').exists())

    def test_book_perform_update_method(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        book_title = 'Tytuł tom 2'
        response_update_book = client.patch(self.book_detail_url, {'title': book_title}, format='json')
        self.assertEqual(response_update_book.status_code, 200)
        self.assertTrue(Book.objects.filter(title=book_title, editor=self.user2).exists())

    def test_book_perform_update_method_with_anonymous(self):
        client = APIClient()
        book_title = 'Tytuł tom 2'
        response_update_book = client.patch(self.book_detail_url, {'title': book_title}, format='json')
        self.assertEqual(response_update_book.status_code, 403)
        self.assertFalse(Book.objects.filter(title=book_title).exists())

    def test_book_action_show_available_books(self):
        client = APIClient()
        response_available_books = client.get(self.book_available_action_url)  # data
        self.assertEqual(response_available_books.status_code, 200)
        queryset = Book.objects.filter(status=True)
        serializer = BookSerializer(queryset, many=True)
        self.assertEqual(len(response_available_books.data), len(queryset))
        self.assertEqual(response_available_books.data, serializer.data)

    def test_book_perform_destroy_method(self):
        client = APIClient()
        client.force_authenticate(self.user)
        response_destroy_book = client.delete(self.book_detail_url)
        self.assertEqual(response_destroy_book.status_code, 204)

    def test_book_perform_destroy_method_for_anonymous(self):
        client = APIClient()
        response_destroy_book = client.delete(self.book_detail_url)
        self.assertEqual(response_destroy_book.status_code, 403)
