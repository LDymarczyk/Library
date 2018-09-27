from django.db import models
from .user import Reader
from .book import Book
from .library import Library


class Rent(models.Model):
    creator = models.ForeignKey(Reader, related_name='rent_creator', editable=False, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True, editable=False)
    end_date = models.DateField(null=True, blank=True)
    reader = models.ForeignKey(Reader,related_name='rent_reader', on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='book_to_rent')
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True) #?
    status = models.BooleanField(null=True, blank=True)

    def custom_id(self):
        self.id += 10000

    def get_book(self):
        return self.book

    def return_book(self):
        self.status = False

    def make_rent(self):
        self.status = True

    class Meta:
        order_with_respect_to = 'reader'
