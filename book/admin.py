from django.contrib import admin
from .models.page import Page
from .models.book import Book


admin.site.register(Book)
admin.site.register(Page)
