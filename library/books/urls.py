from django.urls import path
from .views.authors_list import AuthorList
from .views.books_list import BookList
from .views.libraries_list import LibraryList
from .views.rents_list import RentList
from .views.users_list import UserList
from .views.author_details import AuthorDetail

urlpatterns = [
    path('authors/', AuthorList.as_view()),
    path('books/', BookList.as_view()),
    path('libraries/', LibraryList.as_view()),
    path('rents/', RentList.as_view()),
    path('users/', UserList.as_view()),
    path('authors/<int:pk>/', AuthorDetail.as_view()),
]