from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register('category', views.CategoryViewSet, basename='Category')
router.register('transactions', views.TransactionViewSet, basename='Transaction')
router.register('widget', views.WidgetViewSet, basename='Widget')
