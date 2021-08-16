from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register('category', views.CategoryView, basename='Category')
router.register('transactions', views.TransactionViewSet, basename='Transaction')
