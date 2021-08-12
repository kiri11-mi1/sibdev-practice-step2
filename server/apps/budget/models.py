from django.db import models
from apps.users.models import User
from datetime import date

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(verbose_name='Сумма',max_digits=15, decimal_places=2, default=0)
    date = models.DateField(verbose_name='Дата операции', default=date.today)

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = u'Транзакция'
        verbose_name_plural = u'Транзакции'

