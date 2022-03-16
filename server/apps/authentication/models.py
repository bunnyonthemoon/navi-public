from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

import env
from apps.authentication.managers import UserManager

from . import scripts


class User(AbstractUser):
    email = models.EmailField(unique=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

