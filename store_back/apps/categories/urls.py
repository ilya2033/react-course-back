from django.urls import path
from . import views


app_name = 'categories'

#Шаблоны ссылок данного приложения
urlpatterns = [
	path('categories/',views.category_list, name = 'category_list'),
    path('categories/<str:_id>/',views.category_detail, name = 'category_detail'),
    path('category/<str:_id>/delete/',views.category_delete, name = 'category_delete'),
    path('category/',views.category_upsert, name = 'category_upsert'),

]