from django.test import TestCase
from books.models import Rent

class RentModelTests(TestCase):

    def test_custom_id(self):
        rent = Rent(id=500)
        rent.custom_id()
        self.assertEqual(rent.id, 10500)