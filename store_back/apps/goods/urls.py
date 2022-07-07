from django.urls import path
from . import views


app_name = 'goods'

#Шаблоны ссылок данного приложения
urlpatterns = [
	path('goods/',views.good_list, name = 'good_list'),
    path('goods/<str:_id>/',views.good_detail, name = 'good_detail'),
    path('good/<str:_id>/delete/',views.good_delete, name = 'good_delete'),
    path('good/',views.good_upsert, name = 'good_upsert'),
   
]