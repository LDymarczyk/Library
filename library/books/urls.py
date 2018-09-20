from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views.author import AuthorViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
