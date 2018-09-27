from django.test import TestCase
from books.models import Author

class AuthorModelTests(TestCase):

    def test_get_full_name(self):
        #import pdb; pdb.set_trace()
        author = Author(first_name = "Ala", last_name = "MaKota")
        self.assertEqual(author.get_full_name(), "Ala MaKota")

    def test_get_first_name(self):
        author = Author(first_name="Ala")
        self.assertEqual(author.get_first_name(), "Ala")

    def test_get_last_name(self):
        author = Author(last_name="MaKota")
        self.assertEqual(author.get_last_name(), "MaKota")

    def test_get_birth_year(self):
        author = Author(birth_year=1999)
        self.assertEqual(author.get_birth_year(), 1999)

    def test_get_death_year(self):
        author = Author(death_year=2000)
        self.assertEqual(author.get_death_year(), 2000)