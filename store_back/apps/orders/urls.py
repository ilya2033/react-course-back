from django.urls import path
from . import views


app_name = 'orders'

#Шаблоны ссылок данного приложения
urlpatterns = [
	path('orders/',views.order_list, name = 'order_list'),
    path('orders/<str:_id>/',views.order_detail, name = 'order_detail'),
    path('order/',views.order_upsert, name = 'order_upsert'),
    path('order/<str:_id>/delete/',views.order_delete, name = 'order_delete'),

]