from django.db import models
from .author import Author
from .user import Reader
from .library import Library


class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(Reader, editable=False, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    ISBN = models.IntegerField()
    genre = models.CharField(max_length=100)
    edition = models.IntegerField()
    amount = models.IntegerField()
    publication_date = models.DateField()
    publishing_house = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    status = models.BooleanField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)

    class Meta:
        app_label = 'books'
