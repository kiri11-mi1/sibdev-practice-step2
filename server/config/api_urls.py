from re import I
from django.urls import include, path
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url('users/', include('apps.users.urls')),
    url('budget/', include('apps.budget.urls'))
]
