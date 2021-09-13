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


class WidgetSerializer(serializers.ModelSerializer):
    amount = fields.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    duration = serializers.DurationField()
    end_date = fields.SerializerMethodField()

    def get_end_date(self, obj):
        return obj.created + obj.duration

    class Meta:
        model = models.Widget
        fields = ('id', 'owner', 'category', 'limit', 'duration', 'criterion', 'color', 'created', 'amount', 'end_date',)
