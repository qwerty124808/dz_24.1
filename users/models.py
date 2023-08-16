from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=150, verbose_name='телефон')
    city = models.CharField(max_length=150, verbose_name='город')
    avatar = models.ImageField(upload_to='', verbose_name='аватарка' ,**NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []