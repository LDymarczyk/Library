from rest_framework.test import APITestCase, APIRequestFactory
from ...models import Author, Book, Library, Reader, Rent
from ...serializers.rent import RentSerializer
from rest_framework.exceptions import ValidationError, ErrorDetail
from datetime import datetime, date

def make_random_number():
    today = datetime.today()
    return str(today.hour) + str(today.min) + str(today.second) +str(today.microsecond)

class RentSerializersTests(APITestCase):

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
                                              name='Biblioteka ' + make_random_number(),
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

        self.rent_attrs = {'start_date' : date(2018,10,20),
                            'end_date' : date(2018,11,8),
                            'reader' : self.user,
                            'book' : self.book}

        self.rent = Rent.objects.create(**self.rent_attrs)

        self.factory = APIRequestFactory()

    def test_contains_expected_fields_book_serializer(self):
        data = RentSerializer(instance=self.rent)
        self.assertCountEqual(data.fields, {'end_date',
                                            'start_date',
                                            'reader',
                                            'book',
                                            'library'
                                            })

    def test_validate_with_correct_values(self):
        self.rent_attrs['reader']=self.user.pk
        self.rent_attrs['book']=self.book.pk
        serializer = RentSerializer(instance=self.rent, data=self.rent_attrs)
        self.assertTrue(serializer.is_valid())

    def test_validate_with_non_existing_book(self):
        self.rent_attrs['book'] = self.book.pk + 500000
        serializer = RentSerializer(instance=self.rent, data=self.rent_attrs)
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['book'][0]
        self.assertEqual(ErrorDetail(string='Invalid pk "' + str(self.book.pk + 500000) + '" - object does not exist.', code='does_not_exist'), error)
        self.assertFalse(serializer.is_valid())

    def test_validate_with_non_existing_reader(self):
        self.rent_attrs['reader'] = self.user.pk + 500000
        serializer = RentSerializer(instance=self.rent, data=self.rent_attrs)
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['reader'][0]
        self.assertEqual(ErrorDetail(string='Invalid pk "' + str(self.user.pk + 500000) + '" - object does not exist.', code='does_not_exist'), error)
        self.assertFalse(serializer.is_valid())

    def test_validate_with_bad_dates(self):
        self.rent_attrs['reader'] = self.user.pk
        self.rent_attrs['book'] = self.book.pk
        self.rent_attrs['start_date'] = date(2018, 12, 10)
        self.rent_attrs['end_date'] = date(2018, 10, 10)
        serializer = RentSerializer(instance=self.rent, data=self.rent_attrs)
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        error = cm.exception.args[0]['non_field_errors'][0]
        self.assertEqual('End date must be later than start date.', error)
        self.assertFalse(serializer.is_valid())

