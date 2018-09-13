from django.db import models
from .user import Reader
from .book import Book
from .library import Library


class Rent(models.Model):
    creator = models.ForeignKey(Reader, related_name='rent_creator', editable=False, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True, editable=False)
    end_date = models.DateTimeField()
    reader = models.ForeignKey(Reader,related_name='rent_reader', on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True) #?
    rent_id = models.IntegerField(default=0)

    def custom_id(self):
        self.rent_id = self.id + 10000

    class Meta:
        app_label = 'books'

