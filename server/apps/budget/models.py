from django.db import models
from apps.users.models import User
from datetime import date
from colorfield.fields import ColorField


class Category(models.Model):
    TYPES = (
        (0, 'Доход'),
        (1, 'Расход')
    )
    name = models.CharField(verbose_name='Название', max_length=128)
    type = models.PositiveSmallIntegerField('Тип', choices=TYPES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class Transaction(models.Model):
    owner = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Владелец')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(verbose_name='Сумма', max_digits=15, decimal_places=2, default=0)
    date = models.DateField(verbose_name='Дата операции', default=date.today)

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = u'Транзакция'
        verbose_name_plural = u'Транзакции'


class Widget(models.Model):
    CRITERION = [
        ('>', 'Больше'),
        ('<', 'Меньше'),
    ]
    owner = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Владелец')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    limit = models.DecimalField(verbose_name='Лимит суммы', max_digits=15, decimal_places=2, default=0)
    duration = models.DurationField(verbose_name='Срок действия')
    criterion = models.CharField(verbose_name='Критерий', choices=CRITERION, max_length=2)
    color = ColorField(verbose_name='Цвет', default='#FF0000')
    created = models.DateField(verbose_name='Дата создания', default=date.today)

    def __str__(self):
        return str(self.criterion) + ' ' + str(self.limit) + ' ' + str(self.category)

    class Meta:
        verbose_name = u'Виджет'
        verbose_name_plural = u'Виджеты'
