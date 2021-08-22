from django_filters import rest_framework as filters

from .models import Transaction


class TransactionFilter(filters.FilterSet):
    start_date = filters.NumberFilter(field_name="date", lookup_expr='gte')
    end_date = filters.NumberFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['date', 'start_date', 'end_date']
