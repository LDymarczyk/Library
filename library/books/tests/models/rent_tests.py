from rest_framework.test import APITestCase
from books.models import Rent, Book, Author, Library, Reader
from datetime import date


class RentModelTests(APITestCase):

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
                                              name='Biblioteka 1',
                                              phone='123456789')

        self.book = Book.objects.create(title='title1',
                                        id=5,
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

        self.rent = Rent.objects.create(start_date=date(2018, 10, 8),
                                        end_date=date(2019, 11, 8),
                                        reader=self.user,
                                        book=self.book,
                                        )

        self.rent2 = Rent.objects.create(start_date=date(2018, 3, 8),
                                        end_date=date(2018, 10, 8),
                                        reader=self.user,
                                        book=self.book,
                                        )

    def test_custom_id(self):
        id = self.rent.id
        self.rent.custom_id()
        self.assertEqual(self.rent.id, 10000+id)

    def test_get_book(self):
        self.assertEqual(self.rent.get_book().id, 5)

    def test_make_rent(self):
        self.rent.make_rent()
        self.assertTrue(self.rent.status)

    def test_return_book(self):
        #import pdb; pdb.set_trace()
        self.rent.return_book()
        self.assertFalse(self.rent.status)

    def test_calculate_payment(self):
        self.rent2.calculate_payment()
        self.assertEqual(self.rent2.cost/2, (date.today() - self.rent2.end_date).days )