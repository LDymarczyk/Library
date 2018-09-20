from django.urls import path
from django.conf.urls import url
from .views.authors_list import AuthorList
from .views.api_root import api_root
from .views.books_list import BookList
from .views.libraries_list import LibraryList
from .views.rents_list import RentList
from .views.users_list import UserList
from .views.author_details import AuthorDetail
from .views.book_details import BookDetail
from .views.library_details import LibraryDetail
from .views.rent_details import RentDetail
from .views.user_details import UserDetail
from .views.author_filter import AuthorFilter
from . import views
# from .views.authors_list import AuthorListF

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'authors/', AuthorList)

urlpatterns = [
    url(r'^$', api_root),
    # path('authors/', AuthorList, name='authors-list'),
    # url('^authors/(?P<first_name>.+)/$', AuthorFilter.as_view()),
    path('books/', BookList.as_view(), name='books-list'),
    path('libraries/', LibraryList.as_view(), name='libraries-list'),
    path('rents/', RentList.as_view(), name='rents-list'),
    path('users/', UserList.as_view(), name='users-list'),
    # path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-details'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-details'),
    path('libraries/<int:pk>/', LibraryDetail.as_view(), name='library-details'),
    path('rents/<int:pk>/', RentDetail.as_view(), name='rent-details'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-details'),
    # url(r'^list$', AuthorListF.as_view())
]
urlpatterns += router.urls
