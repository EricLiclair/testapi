from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

import string
import random

from rest_framework.authentication import TokenAuthentication

# unique user id which will be mapped with user profiles


def generate_unique_id() -> str:
    length: int = 9
    while True:
        id: str = ''.join(random.choices(string.ascii_uppercase, k=length))
        try:
            if User.objects.filter(id=id).count() == 0:
                break
        except:
            return id
    return id


class User(AbstractUser):
    id = models.CharField(
        _('id'),
        max_length=16,
        default=generate_unique_id,
        primary_key=True,
        editable=False
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.username
