# Generated by Django 3.2.2 on 2021-08-12 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Сумма'),
        ),
    ]
