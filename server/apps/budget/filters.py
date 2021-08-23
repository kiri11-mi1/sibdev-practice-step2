from django_filters import rest_framework as filters

from .models import Transaction, Category


class CategoryFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="transaction__date")
    start_date = filters.DateFilter(field_name="transaction__date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="transaction__date", lookup_expr='lte')

    class Meta:
        model = Category
        fields = ['date', 'start_date', 'end_date']


class TransactionFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="date")
    start_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['date', 'start_date', 'end_date']
