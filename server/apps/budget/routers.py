from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register('category', views.CategoryView)
router.register('transactions', views.TransactionViewSet)
