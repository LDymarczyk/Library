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

        self.rent = Rent.objects.create(start_date=date(2018,10,8),
                                        end_date=date(2018,11,8),
                                        reader=self.user,
                                        book=self.book)

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
        user, book = self.user, self.book
        data = {'start_date' : date(2018,10,8),
                'end_date' : date(2018,11,8),
                'reader' : user.pk,
                'book' : book.pk}
        request = self.factory.get('/')
        request.user = self.user
        serializer = RentSerializer(data=data, context={'request': request})
        #import pdb; pdb.set_trace()
        self.assertTrue(serializer.is_valid())
    #
    # def test_validate_with_bad_email(self):
    #     data = {'address':"aaaaaaa",
    #             'email':"email",
    #             'name':"aaaaaaa"+make_random_number(),
    #             'phone':"123456789"}
    #     request = self.factory.get('/')
    #     request.user = self.user
    #     serializer = LibrarySerializer(data=data, context={'request': request})
    #     with self.assertRaises(ValidationError) as cm:
    #         serializer.is_valid(raise_exception=True)
    #     error = cm.exception.args[0]['email'][0]
    #     self.assertEqual(ErrorDetail(string='Enter a valid email address.', code='invalid'), error)
    #     self.assertFalse(serializer.is_valid())