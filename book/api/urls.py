from django.urls import path
from .views.book import BookView
from .views.page import PageView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("book/", csrf_exempt(BookView.as_view()), name="book-list"),
    path("book/<int:pk>/", csrf_exempt(BookView.as_view()), name="book-detail"),
    path("book/<int:id>/page/", PageView.as_view(), name="book-list"),
    path("book/<int:id>/page/<int:pk>/", PageView.as_view(), name="book-detail"),
]
