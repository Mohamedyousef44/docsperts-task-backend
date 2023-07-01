from .time_stamp import TimeStampedModel
from django.db import models


class Book(TimeStampedModel):
    author = models.ForeignKey("user.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.title}"
