from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views.author import AuthorViewSet
from .views.book import BookViewSet
from .views.library import LibraryViewSet
from .views.rent import RentViewSet
from .views.user import UserViewSet


router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'libraries', LibraryViewSet)
router.register(r'rents', RentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
