import re
from django.utils import translation
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Value, DecimalField, Q
from django.db.models.functions import Coalesce

from . import models
from . import serializers
from .pagination import StandardResultsSetPagination


class CategoryView(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        queryset = models.Category.objects.all()
        if self.action == 'get_all_categories_info':
            queryset = queryset.annotate(
                amount=Coalesce(
                    Sum('transaction__amount'), 
                    Value(0),
                    output_field=DecimalField()
                )
            )
        return queryset

    @action(detail=False, methods=['GET'])
    def get_all_categories_info(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TransactionSerializer
    pagination_class = StandardResultsSetPagination
    queryset = models.Transaction.objects.all()

    @action(detail=False, methods=['GET'])
    def global_info(self, request):
        amount_by_categories = self.queryset.aggregate(
            income=Coalesce(
                Sum(
                    'amount', 
                    filter=Q(category__type=0),
                ), 
                Value(0),
                output_field=DecimalField(),
            ),
            expense=Coalesce(
                Sum(
                    'amount',
                    filter=Q(category__type=1),
                ),
                Value(0),
                output_field=DecimalField(),
            )
        )
        return Response(amount_by_categories)
