from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register('category', views.CategoryViewSet, basename='category')
router.register('transactions', views.TransactionViewSet, basename='transaction')
router.register('widget', views.WidgetViewSet, basename='widget')
