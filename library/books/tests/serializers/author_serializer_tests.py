from rest_framework.test import APITestCase, APIRequestFactory
from ...models import Author, Reader
from ...serializers.author import AuthorSerializer
from rest_framework.exceptions import ValidationError

class AuthorSerializersTests(APITestCase):

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

        self.factory = APIRequestFactory()

    def test_contains_expected_fields_author_serializer(self):
        data = AuthorSerializer(instance=self.author)
        self.assertCountEqual(data.fields, {'first_name', 'last_name',
                                            'birth_year', 'death_year',
                                            'id', 'creator', 'created'
                                            })

    def test_validate_with_valid_author(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Kowalski',
                'birth_year' : 1990, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        self.assertTrue(serializer.is_valid())

    def test_validate_author_serializer_with_too_short_first_name(self):
        data = {'first_name' : 'A', 'last_name' : 'Kowalski',
                'birth_year' : 1990, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['first_name'][0]
        self.assertEqual("First name must be longer than 3 letters.",
                         error)
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_with_too_long_first_name(self):
        data = {'first_name' : 'A'*60, 'last_name' : 'Kowalski',
                'birth_year' : 1990, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['first_name'][0]
        self.assertEqual("The longest name in the world is: RhoshandiatellyneshiaunneveshenkKoyaanisquatsiuth (57 letters), please enter some shorter.",
                         error)
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_with_too_short_last_name(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Ko',
                'birth_year' : 1990, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['last_name'][0]
        self.assertEqual("Last name must be longer than 3 letters.",
                         error)
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_with_too_long_last_name(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Ko'*30,
                'birth_year' : 1990, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['last_name'][0]
        self.assertEqual("Please enter shorter last name.",
                         error)
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_with_bad_birth_year(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Kowalski',
                'birth_year' : 1000, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['birth_year'][0]
        self.assertEqual("Birth year must be greater than 1400. Printing was invented in 1450.",
                         error)
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_with_future_birth_year(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Kowalski',
                'birth_year' : 5000, 'death_year' : 2013}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['birth_year'][0]
        self.assertEqual("Author doesn't born yet.",
                         error)
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_with_earlier_death_than_birth_year(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Kowalski',
                'birth_year' : 1900, 'death_year' : 1800}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['non_field_errors'][0]
        self.assertEqual("People can't die before their birth. Wrong birth/death years.",
                         error)
        self.assertFalse(serializer.is_valid())

    def test_validate_author_serializer_author_died_too_young_to_be_an_author(self):
        data = {'first_name' : 'Adam', 'last_name' : 'Kowalski',
                'birth_year' : 1900, 'death_year' : 1901}
        request = self.factory.get('/')
        request.user = self.user
        serializer = AuthorSerializer(data=data, context={'request':request})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['non_field_errors'][0]
        self.assertEqual("Some people are geniuses, but I don't think they can write a book before they are 10.",
                         error)
        self.assertFalse(serializer.is_valid())



