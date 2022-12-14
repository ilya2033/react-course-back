from django.urls import path
from . import views

from rest_framework_simplejwt.views import (  TokenRefreshView)
from .views import MyTokenObtainPairView


app_name = 'auth'

#Шаблоны ссылок данного приложения
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.register, name = "register"),

]