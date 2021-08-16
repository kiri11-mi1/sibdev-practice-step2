from rest_framework import serializers, fields

from . import models


class CategorySerializer(serializers.ModelSerializer):
    amount = fields.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'type', 'owner', 'amount')


class TransactionSerializer(serializers.ModelSerializer):
    category_type = fields.IntegerField(source='category.type', read_only=True)

    class Meta:
        model = models.Transaction
        fields = ('id', 'owner', 'amount', 'date', 'category', 'category_type',)
