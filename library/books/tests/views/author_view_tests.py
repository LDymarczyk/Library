from rest_framework.test import APIClient, APITestCase
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

        self.author_list_url = '/authors/'
        self.author_detail_url = '/authors/{}/'.format(self.author.pk)

    def test_author_perform_create_method(self):
        client = APIClient()
        client.force_authenticate(self.user)
        response_create_author = client.post(self.author_list_url, self.author_attrs, format='json')
        self.assertEqual(response_create_author.status_code, 201)
        self.assertTrue(Author.objects.filter(first_name="Adam", creator=self.user).exists())

    def test_author_perform_create_method_for_anonymous(self):
        client = APIClient()
        self.author_attrs['first_name'] = 'Not Adam'
        response_create_author = client.post(self.author_list_url, self.author_attrs, format='json')
        self.assertEqual(response_create_author.status_code, 403)
        self.assertFalse(Author.objects.filter(first_name="Not Adam").exists())

    def test_author_perform_update_method(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        author_first_name = 'Krzysztof'
        response_modify_author = client.patch(self.author_detail_url, {'first_name': author_first_name}, format='json')
        self.assertEqual(response_modify_author.status_code, 200)
        self.assertTrue(Author.objects.filter(first_name=author_first_name, editor=self.user2).exists())

    def test_author_perform_update_method_for_anonymous(self):
        client = APIClient()
        author_first_name = 'Franek'
        response_modify_author = client.patch(self.author_detail_url, {'first_name': author_first_name}, format='json')
        self.assertEqual(response_modify_author.status_code, 403)
        self.assertFalse(Author.objects.filter(first_name=author_first_name).exists())
