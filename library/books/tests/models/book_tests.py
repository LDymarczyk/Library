from django.test import TestCase
from books.models import Book

class BookModelTests(TestCase):

    def test_rent_book(self):
        book = Book(amount=10)
        book.rent_book()
        self.assertEqual(book.amount, 9)

    def test_return_book(self):
        book = Book(amount=10)
        book.return_book()
        self.assertEqual(book.amount, 11)

    def test_is_rented(self):
        book = Book(amount=10, status=True)
        self.assertTrue(book.is_rented())

    def test_last_book_rented(self):
        book = Book(amount=1)
        book.rent_book()
        self.assertFalse(book.is_rented())

    def test_return_missing_book(self):
        book = Book(amount=0)
        book.return_book()
        self.assertTrue(book.is_rented())

    def test_add_more_books(self):
        book = Book(amount=10)
        book.add_more_books(2)
        self.assertEqual(book.amount, 12)

