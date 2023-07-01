from .time_stamp import TimeStampedModel
from django.db import models
from .book import Book


class Page(TimeStampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_number = models.PositiveIntegerField()
    content = models.TextField()

    def __str__(self):
        return f"{self.page_number}"
