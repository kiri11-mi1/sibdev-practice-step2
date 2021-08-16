from django.contrib import admin
from . import models


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'owner', 'date']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'type']
