from django.db import models
from .user import User
from .book import Book
from .library import Library


class Rent(models.Model):
    creator = models.ForeignKey(User, editable=False)
    start_date = models.DateTimeField(auto_now_add=True, editable=False)
    end_date = models.DateTimeField()
    reader = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    library = models.ForeignKey(Library) #?