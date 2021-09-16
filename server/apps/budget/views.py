from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from django.db.models import Sum, Value, DecimalField, Q
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from . import models, filters, serializers, docs
from .pagination import StandardResultsSetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = models.Category.objects.all()
        if self.action == 'get_all_categories_info':
            self.filter_backends = (DjangoFilterBackend,)
            self.filterset_class = filters.CategoryFilter
            queryset = self.filter_queryset(
                queryset.annotate(
                    amount=Coalesce(
                        Sum('transaction__amount'),
                        Value(0),
                        output_field=DecimalField()
                    )
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

    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.filter_queryset(models.Transaction.objects.all())

    @swagger_auto_schema(**docs.swagger_global_info)
    @action(detail=False, methods=['GET'])
    def global_info(self, request):
        queryset = self.get_queryset().aggregate(
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
        return Response(queryset)


class WidgetViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WidgetSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = models.Widget.objects.all()
        if self.action == 'list':
            queryset = queryset.annotate(
                amount=Coalesce(
                    Sum('category__transaction__amount'),
                    Value(0),
                    output_field=DecimalField()
                )
            )
        return queryset
