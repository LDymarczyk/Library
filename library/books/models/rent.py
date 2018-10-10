from django.db import models
from .user import Reader
from .book import Book
from .library import Library
from datetime import date


class Rent(models.Model):
    creator = models.ForeignKey(Reader, related_name='rent_creator', editable=False, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    reader = models.ForeignKey(Reader,related_name='rent_reader', on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='book_to_rent')
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True) #?
    status = models.BooleanField(null=True, blank=True)
    late = models.BooleanField(null=True, blank=True)
    regulated_payment = models.BooleanField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)

    def custom_id(self):
        self.id += 10000

    def get_book(self):
        return self.book

    def pay_for_late(self, money):
        self.cost -= money
        if self.cost <= 0.0:
            self.regulated_payment = True
            return "Payment complete."
        return "Reader must pay: " + str(self.cost)

    def return_book(self):
        today = date.today()
        if (self.end_date <= today) or self.regulated_payment:
            self.status = False
        else:
            self.late = True
            self.regulated_payment = False

    def make_rent(self):
        self.status = True
        self.late = False
        self.regulated_payment = False

    class Meta:
        order_with_respect_to = 'reader'
