from django.db import models
from users.models import NULLABLE, User

class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    photo = models.ImageField(upload_to='', verbose_name='превью' ,**NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    user = models.ForeignKey(User,  verbose_name='владелец', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'курс: {self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    photo = models.ImageField(upload_to='', verbose_name='превью' ,**NULLABLE)
    url =  models.URLField(max_length=250, verbose_name='ссылка на видео урок', **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.CASCADE, **NULLABLE)
    user = models.ForeignKey(User, verbose_name='владелец', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'урок: {self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'