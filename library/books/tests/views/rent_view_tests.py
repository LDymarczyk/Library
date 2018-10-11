from rest_framework.test import APIClient, APITestCase
from ...models import Author, Reader, Book, Rent
from datetime import date


class RentPermissionTest(APITestCase):

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

        self.book = Book.objects.create(**self.book_attrs)

        self.rent_attrs = {'start_date': date(2018, 10, 20),
                           'end_date': date(2018, 11, 8),
                           'reader': self.user.pk,
                           'book': self.book.pk}

        self.rent_list_url = '/rents/'
        # self.rent_detail_url = '/rents/{}/'.format(self.rent.pk)

    def test_rent_perform_create_method(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        response_create_rent = client.post(self.rent_list_url, self.rent_attrs, format='json')
        self.assertEqual(response_create_rent.status_code, 201)
        self.assertTrue(Rent.objects.filter(start_date=date(2018, 10, 20), creator=self.superuser).exists())

    def test_rent_perform_create_method_with_anonymous(self):
        client = APIClient()
        response_create_rent = client.post(self.rent_list_url, self.rent_attrs, format='json')
        self.assertEqual(response_create_rent.status_code, 403)
        self.assertFalse(Rent.objects.filter(start_date=date(2018, 10, 20)).exists())

    def test_rent_perform_update_method(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        client.post(self.rent_list_url, self.rent_attrs, format='json')
        rent_detail_url = '/rents/{}/'.format(Rent.objects.all()[0].pk)
        rent_end_date = date(2019, 1, 1)
        response_update_rent = client.patch(rent_detail_url, {'end_date': rent_end_date}, format='json')
        self.assertEqual(response_update_rent.status_code, 200)
        self.assertTrue(Rent.objects.filter(editor=self.user2, end_date=rent_end_date).exists())

    def test_rent_perform_update_method_with_anonymous(self):
        client = APIClient()
        client.force_authenticate(self.user)
        client.post(self.rent_list_url, self.rent_attrs, format='json')
        rent_detail_url = '/rents/{}/'.format(Rent.objects.all()[0].pk)
        rent_end_date = date(2019, 1, 1)
        client.logout()
        response_update_rent = client.patch(rent_detail_url, {'end_date': rent_end_date}, format='json')
        self.assertEqual(response_update_rent.status_code, 403)
        self.assertFalse(Rent.objects.filter(start_date=date(2018, 10, 20), end_date=rent_end_date).exists())
