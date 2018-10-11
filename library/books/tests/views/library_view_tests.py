from rest_framework.test import APIClient, APITestCase
from ...models import Reader, Library
from ..tools import make_random_number


class LibraryPermissionTest(APITestCase):

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

        self.library_attrs = {"name": "aabb",
                              "address": "aa",
                              "phone": "123456789",
                              "email": "lib@mail.com"}

        self.library = Library.objects.create(**self.library_attrs)

        self.library_list_url = '/libraries/'
        self.library_detail_url = '/libraries/{}/'.format(self.library.pk)

    def test_library_perform_create_method(self):
        client = APIClient()
        client.force_authenticate(self.user)
        self.library_attrs["name"] = self.library_attrs["name"] + make_random_number()
        response_create_library = client.post(self.library_list_url, self.library_attrs, format='json')
        self.assertEqual(response_create_library.status_code, 201)
        self.assertTrue(Library.objects.filter(address="aa", creator=self.user).exists())

    def test_library_perform_create_method_with_anonymous(self):
        client = APIClient()
        self.library_attrs["name"] = self.library_attrs["name"] + make_random_number()
        response_create_library = client.post(self.library_list_url, self.library_attrs, format='json')
        self.assertEqual(response_create_library.status_code, 403)
        self.assertFalse(Library.objects.filter(address="aa", creator=self.user).exists())

    def test_library_perform_update_method(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        library_name = "SoLibrary"
        response_update_library = client.patch(self.library_detail_url, {"name": library_name}, format='json')
        self.assertEqual(response_update_library.status_code, 200)
        self.assertTrue(Library.objects.filter(name=library_name, editor=self.user2).exists())

    def test_library_perform_update_method_with_anonymous(self):
        client = APIClient()
        library_name = "SoLibrary"
        response_update_library = client.patch(self.library_detail_url, {"name": library_name}, format='json')
        self.assertEqual(response_update_library.status_code, 403)
        self.assertFalse(Library.objects.filter(name=library_name).exists())
