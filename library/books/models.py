from django.db import models


class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_leght=100)
    ISBN = models.IntegerField(MinValueValidator=1000000000000, MaxValueValidator=9999999999999)
    genre = models.CharField(max_lenght=100)
    edition = models.IntegerField(MinValueValidator=1)
    amount = models.IntegerField(MinValueValidator=0)
    publication_date = models.DateField()
    publishing_house = models.CharField(max_lenght=100)
    language = models.CharField(max_lenght=100)
    status = models.BooleanField()
    author = models.ForeignKey('Author', on_delete=models.)


class Author(models.Model):
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    birth_year = models.IntegerField(MinValueValidator=1500)
    death_year = models.IntegerField(MinValueValidator=1500)

