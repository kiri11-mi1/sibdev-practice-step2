from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserView.as_view()),
    path('me/', views.AboutUserView.as_view())
]
