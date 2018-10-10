from rest_framework.test import APIClient, APITestCase
from ...models import Author, Reader, Book


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

        self.book = Book.objects.create(**self.book_attrs)

        self.book_list_url = '/books/'
        self.book_detail_url = '/books/{}/'.format(self.book.pk)

    def test_book_perform_create_method(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        self.book_attrs['author']=self.author.pk
        response_create_book = client.post(self.book_list_url, self.book_attrs, format='json')
        self.assertEqual(response_create_book.status_code, 201)
        self.assertTrue(Book.objects.filter(title='Tytuł tom 1', creator=self.superuser).exists())

    def test_book_perform_create_method_with_anonymous(self):
        client = APIClient()
        self.book_attrs['author']=self.author.pk
        response_create_book = client.post(self.book_list_url, self.book_attrs, format='json')
        self.assertEqual(response_create_book.status_code, 403)
        self.assertFalse(Book.objects.filter(title='Tytuł tom 1', creator=self.user).exists())

    def test_book_perform_update_method(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        book_title='Tytuł tom 2'
        response_update_book = client.patch(self.book_detail_url, {'title': book_title},format='json')
        self.assertEqual(response_update_book.status_code, 200)

    def test_book_perform_update_method_with_anonymous(self):
        client = APIClient()
        book_title='Tytuł tom 2'
        response_update_book = client.patch(self.book_detail_url, {'title': book_title},format='json')
        self.assertEqual(response_update_book.status_code, 403)


