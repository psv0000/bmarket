from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    purse = models.PositiveSmallIntegerField(default=50, verbose_name='Кошелек')

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
