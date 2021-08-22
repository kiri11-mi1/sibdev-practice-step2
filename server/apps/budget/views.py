import re
from django.utils import translation
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Value, DecimalField, Q
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from . import serializers
from .pagination import StandardResultsSetPagination
from . import filters


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

    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.TransactionFilter

    def get_queryset(self):
        queryset = models.Transaction.objects.all()
        if self.action == 'global_info':
            queryset = queryset.aggregate(
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
        return queryset

    @action(detail=False, methods=['GET'])
    def global_info(self, request):
        return Response(self.get_queryset())
