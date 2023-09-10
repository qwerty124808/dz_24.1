from django.db import models
from users.models import NULLABLE, User

class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    photo = models.ImageField(upload_to='', verbose_name='превью' ,**NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    user = models.ForeignKey(User,  verbose_name='владелец', related_name="courses", on_delete=models.CASCADE, **NULLABLE)

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
    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.CASCADE, related_name="lessons", **NULLABLE)
    user = models.ForeignKey(User, verbose_name='владелец', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'урок: {self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

class Payment(models.Model):
    CHOICES = (
        ("Card", "карта"),
        ("CASH", "наличка"),
    )

    date_of_payment = models.DateTimeField(verbose_name="дата платежа", auto_now=True)
    course_name = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE)
    lesson_name = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE)
    pay_sum = models.IntegerField(verbose_name="сумма платежа")
    payment_type = models.CharField(choices=CHOICES, verbose_name="тип оплаты")
    user = models.ForeignKey(User, verbose_name='владелец', on_delete=models.CASCADE, **NULLABLE)
    

    def __str__(self):
        return f"{self.user} {self.course_name}"

    class Meta:
        verbose_name = "оплата"
        verbose_name_plural = "оплаты"


class Subscription(models.Model):

    class Meta:
        verbose_name = 'подписка на курс'
        verbose_name_plural = 'подписки на курс'
    course_name = models.CharField(max_length=255, verbose_name='название курса', null=True, blank=True)
    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.CASCADE,related_name='subscriptions', blank=False)
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE,related_name='subscriptions', blank=False)

    def __str__(self):
        return f'{self.course} {self.user}'

    def save(self, *args, **kwargs):
        self.course_name = self.course.name

        return super(Subscription, self).save(*args, **kwargs)