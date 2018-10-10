from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient, APITestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from ...models import Author, Reader


class AuthorPermissionTest(APITestCase):

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

        self.author_list_url = '/authors/'

    def test_author_perform_create_method(self):
        client = APIClient()
        client.force_authenticate(self.user)
        response_create_author = client.post(self.author_list_url, self.author_attrs, format='json')
        self.assertEqual(response_create_author.status_code, 201)
        self.assertTrue(Author.objects.filter(first_name="Adam", creator=self.user).exists())
