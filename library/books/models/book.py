from django.db import models
from .author import Author
from .user import Reader
from .library import Library

GENRE_CHOICES = (
    ('FS', "Fantasy"),
    ('SF', "Science-fiction"),
    ('CR', "Criminal"),
    ('RM', "Romance"),
    ('CM', "Comedy"),
)

PUBL_HOUSE = (
    ('FS', 'Fabryka Słów'),
    ('AL', 'Albatros'),
    ('MA', 'MAG')
)


class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(Reader, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    ISBN = models.PositiveIntegerField()
    genre = models.CharField(max_length=2, choices=GENRE_CHOICES, default='FS')
    edition = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    publication_date = models.PositiveIntegerField()
    publishing_house = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    status = models.BooleanField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.id)

    #def



