from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    patronymic = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='Отчество'
    )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

