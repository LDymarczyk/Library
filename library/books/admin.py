from django.contrib import admin
from .models.author import Author
from .models.book import Book
from .models.library import Library
from .models.rent import Rent
from .models.user import Reader


admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Rent)
admin.site.register(Reader)