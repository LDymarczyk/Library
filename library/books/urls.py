from django.urls import path
from .views.authors_list import AuthorList
from .views.books_list import BookList
from .views.libraries_list import LibraryList
from .views.rents_list import RentList

urlpatterns = [
    path('authors/', AuthorList.as_view()),
    path('books/', BookList.as_view()),
    path('libraries/', LibraryList.as_view()),
    path('rents/', RentList.as_view()),
]