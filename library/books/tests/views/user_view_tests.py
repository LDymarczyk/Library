from rest_framework.test import APIClient, APITestCase
from ...models import Author, Reader, Book, Rent
from datetime import date
from ...serializers.rent import RentSerializer


class UserPermissionTest(APITestCase):

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
                           'end_date': date(2020, 10, 8),
                           'reader': self.user,
                           'book': self.book}

        self.rent2_attrs = {'start_date': date(2018, 8, 20),
                            'end_date': date(2018, 9, 1),
                            'reader': self.user,
                            'book': self.book}

        self.rent3_attrs = {'reader': self.user2,
                            'book': self.book}

        self.rent4_attrs = {'reader': self.user2,
                            'book': self.book}

        self.rent5_attrs = {'reader': self.user,
                            'book': self.book}

        self.rent = Rent.objects.create(**self.rent_attrs)
        self.rent2 = Rent.objects.create(**self.rent2_attrs)

        self.user2_rents_url='/users/{}/user_rents/'.format(self.user2.pk)
        self.user2_currently_rented = '/users/{}/currently_rented/'.format(self.user2.pk)

    def test_user_action_user_rents(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        response_user_rents = client.get(self.user2_rents_url)
        self.assertEqual(response_user_rents.status_code, 200)
        queryset = Rent.objects.filter(reader=self.user2)
        serializer = RentSerializer
        self.assertEqual(len(response_user_rents.data), len(queryset))
        queryset = serializer(queryset, many=True)
        self.assertEqual(response_user_rents.data, queryset.data)

    def test_user_action_currently_rented(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        response_currently_rented = client.get(self.user2_currently_rented)
        self.assertEqual(response_currently_rented.status_code, 200)
        queryset = Rent.objects.filter(reader=self.user2, status=True)
        serializer = RentSerializer
        self.assertEqual(len(response_currently_rented.data), len(queryset))
        queryset = serializer(queryset, many=True)
        self.assertEqual(response_currently_rented.data, queryset.data)

