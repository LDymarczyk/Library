from django.test import TestCase
from books.models import Rent
from books.models import Book

class RentModelTests(TestCase):

    def test_custom_id(self):
        rent = Rent(id=500)
        rent.custom_id()
        self.assertEqual(rent.id, 10500)

    def test_get_book(self):
        book = Book(id = 1)
        rent = Rent(book = book)
        self.assertEqual(rent.get_book().id,1)

    def test_make_rent(self):
        rent = Rent()
        rent.make_rent()
        self.assertTrue(rent.status)

    def test_return_book(self):
        rent = Rent()
        rent.return_book()
        self.assertFalse(rent.status)