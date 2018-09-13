from django.db import models
from .author import Author
from .user import User


class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, editable=False)
    title = models.CharField(max_leght=100)
    ISBN = models.IntegerField(MinValueValidator=1000000000000, MaxValueValidator=9999999999999)
    genre = models.CharField(max_lenght=100)
    edition = models.IntegerField(MinValueValidator=1)
    amount = models.IntegerField(MinValueValidator=0)
    publication_date = models.DateField()
    publishing_house = models.CharField(max_lenght=100)
    language = models.CharField(max_lenght=100)
    status = models.BooleanField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT)