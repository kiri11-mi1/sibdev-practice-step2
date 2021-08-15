from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.db.models import DecimalField

from . import models
from . import serializers
from .pagination import StandardResultsSetPagination


class CategoryView(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

    @action(detail=False, methods=['GET'])
    def get_all_categories_info(self, request):
        all_categories = self.queryset.annotate(
            amount=Coalesce(
                Sum('transaction__amount'), 
                Value(0),
                output_field=DecimalField()
            )
        )
        serializer = self.get_serializer(all_categories, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TransactionSerializer
    pagination_class = StandardResultsSetPagination
    queryset = models.Transaction.objects.all()
