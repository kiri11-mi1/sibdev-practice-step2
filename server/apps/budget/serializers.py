from rest_framework import serializers, fields

from . import models


class CategorySerializer(serializers.ModelSerializer):
    sum = fields.IntegerField(read_only=True)

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'type', 'owner', 'sum',)


class TransactionSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(source='category', write_only=True)
    category_type = fields.IntegerField(source='category.type', read_only=True)

    class Meta:
        model = models.Transaction
        fields = ('id', 'owner', 'amount', 'date', 'category', 'category_type',)
