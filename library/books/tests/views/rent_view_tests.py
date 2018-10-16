from rest_framework.test import APIClient, APITestCase
from ...models import Author, Reader, Book, Rent
from datetime import date
from ...serializers.rent import RentSerializer


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
                           'end_date': date(2020, 10, 8),
                           'reader': self.user,
                           'book': self.book}

        self.rent2_attrs = {'start_date': date(2018, 8, 20),
                            'end_date': date(2018, 9, 1),
                            'reader': self.user,
                            'book': self.book}

        self.rent = Rent.objects.create(**self.rent_attrs)
        self.rent2 = Rent.objects.create(**self.rent2_attrs)
        self.rent3 = Rent.objects.create(**self.rent_attrs)

        self.rent_list_url = '/rents/'
        self.rent_detail_url = '/rents/{}/'.format(self.rent.pk)
        self.rent2_detail_url = '/rents/{}/'.format(self.rent2.pk)
        self.rent2_regulate_payment_url = '/rents/{}/regulate_payment/'.format(self.rent2.pk)
        self.rent_current_rents = '/rents/current_rents/'
        self.rent_current_user_rents = '/rents/current_user_rents/'

    def test_rent_perform_create_method(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        attrs = self.rent_attrs
        attrs['book'] = self.book.pk
        attrs['reader'] = self.user.pk
        response_create_rent = client.post(self.rent_list_url, attrs, format='json')
        self.assertEqual(response_create_rent.status_code, 201)
        self.assertTrue(Rent.objects.filter(start_date=date(2018, 10, 20), creator=self.superuser).exists())

    def test_rent_perform_create_method_with_anonymous(self):
        client = APIClient()
        attrs = self.rent_attrs
        attrs['book'] = self.book.pk
        attrs['reader'] = self.user.pk
        attrs['start_date'] = date(2017, 1, 1)
        response_create_rent = client.post(self.rent_list_url, attrs, format='json')
        self.assertEqual(response_create_rent.status_code, 403)
        self.assertFalse(Rent.objects.filter(start_date=date(2017, 1, 1)).exists())

    def test_rent_perform_update_method(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        attrs = self.rent_attrs
        attrs['book'] = self.book.pk
        attrs['reader'] = self.user.pk
        client.post(self.rent_list_url, attrs, format='json')
        rent_detail_url = '/rents/{}/'.format(Rent.objects.all()[0].pk)
        rent_end_date = date(2019, 1, 1)
        response_update_rent = client.patch(rent_detail_url, {'end_date': rent_end_date}, format='json')
        self.assertEqual(response_update_rent.status_code, 200)
        self.assertTrue(Rent.objects.filter(editor=self.user2, end_date=rent_end_date).exists())


    def test_rent_perform_update_method_with_anonymous(self):
        client = APIClient()
        client.force_authenticate(self.user)
        attrs = self.rent_attrs
        attrs['book'] = self.book.pk
        attrs['reader'] = self.user.pk
        client.post(self.rent_list_url, attrs, format='json')
        rent_detail_url = '/rents/{}/'.format(Rent.objects.all()[0].pk)
        rent_end_date = date(2019, 1, 1)
        client.logout()
        response_update_rent = client.patch(rent_detail_url, {'end_date': rent_end_date}, format='json')
        self.assertEqual(response_update_rent.status_code, 403)
        self.assertFalse(Rent.objects.filter(start_date=date(2018, 10, 20), end_date=rent_end_date).exists())

    def test_rent_perform_on_time_destroy_method(self):
        client = APIClient()
        client.force_authenticate(self.user)
        response_destroy_rent = client.delete(self.rent_detail_url)
        #import pdb;pdb.set_trace()
        self.assertEqual(response_destroy_rent.status_code, 204)
        self.assertFalse(Rent.objects.get(pk=self.rent.pk).status)

    def test_rent_perform_destroy_method_for_anonymous(self):
        client = APIClient()
        response_destroy_author = client.delete(self.rent_detail_url)
        self.assertEqual(response_destroy_author.status_code, 403)

    def test_rent_late_perform_destroy_method_rent(self):
        client = APIClient()
        client.force_authenticate(self.user)
        response_destroy_rent = client.delete(self.rent2_detail_url)
        self.assertEqual(response_destroy_rent.status_code, 204)
        self.assertFalse(Rent.objects.get(pk=self.rent2.pk).regulated_payment)
        self.assertTrue(Rent.objects.get(pk=self.rent2.pk).status)
        self.assertTrue(Rent.objects.get(pk=self.rent2.pk).late)
        response_destroy_rent = client.delete(self.rent2_regulate_payment_url)
        self.assertEqual(response_destroy_rent.status_code, 204)
        self.assertTrue(Rent.objects.get(pk=self.rent2.pk).regulated_payment)
        self.assertFalse(Rent.objects.get(pk=self.rent2.pk).status)
        self.assertTrue(Rent.objects.get(pk=self.rent2.pk).late)

    def test_rent_action_current_rents(self):
        client = APIClient()
        client.force_authenticate(self.user)
        response_current_rents = client.get(self.rent_current_rents)
        self.assertEqual(response_current_rents.status_code, 200)
        queryset = Rent.objects.filter(status=True)
        serializer = RentSerializer
        self.assertEqual(len(response_current_rents.data), len(queryset))
        queryset = serializer(queryset, many=True)
        self.assertEqual(response_current_rents.data, queryset.data)

    def test_rent_action_current_user_rents(self):
        client = APIClient()
        client.force_authenticate(self.user)
        response_current_user_rents = client.get(self.rent_current_user_rents)
        self.assertEqual(response_current_user_rents.status_code, 200)
        queryset = Rent.objects.filter(reader=self.user)
        serializer = RentSerializer
        self.assertEqual(len(response_current_user_rents.data), len(queryset))
        queryset = serializer(queryset, many=True)
        self.assertEqual(response_current_user_rents.data, queryset.data)


