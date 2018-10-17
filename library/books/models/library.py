from django.db import models
from . import Reader


class Library(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(Reader, editable=False, on_delete=models.SET_NULL, null=True)
    editor = models.ForeignKey(Reader, related_name='library_editor', editable=False, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def count_books(self):
        books = self.books_library.all()
        #import pdb; pdb.set_trace()
        sum_books = 0
        for book in books:
            if book.library == self:
                sum_books += book.amount
        return sum_books
