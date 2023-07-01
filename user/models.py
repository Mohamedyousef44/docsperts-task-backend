from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.


def validate_min_length(value):
    if len(value) < 8:
        raise ValidationError("The password must be at least 8 characters long.")


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[validate_min_length])
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name}"
