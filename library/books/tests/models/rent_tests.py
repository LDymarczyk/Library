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