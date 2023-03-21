from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = (
        (USER, 'User'),
        (ADMIN, 'Moderator'),
        (MODERATOR, 'Admin')
    )
    email = models.EmailField(
        blank=False,
        max_length=settings.BIG_INT_LENGTH,
        unique=True,
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе',
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=USER,
    )

    class Meta:
        # use ordering, because without we get warning in tests:
        # UnorderedObjectListWarning: Pagination may yield inconsistent
        # results with an unordered object_list
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        if self.username == 'me':
            raise ValidationError(
                'Имя пользователя содержит недопустимый символ'
            )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
