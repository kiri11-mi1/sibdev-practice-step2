from django.contrib import admin
from . import models


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'owner', 'date']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'type']


@admin.register(models.Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['criterion', 'limit', 'category', 'duration', 'owner', 'created']
