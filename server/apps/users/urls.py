from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserCreateView.as_view()),
    path('me/', views.UserInfoView.as_view())
]
