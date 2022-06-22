from django.urls import path
from . import views


app_name = 'goods'

#Шаблоны ссылок данного приложения
urlpatterns = [
	path('goods/',views.good_list, name = 'good_list'),
    path('goods/<str:_id>/',views.good_detail, name = 'good_detail'),
    path('good/<str:_id>/delete/',views.good_delete, name = 'good_delete'),
    path('good/',views.good_upsert, name = 'good_upsert'),
    path('upload/',views.image_upsert, name = 'image_upsert')
    # path('add-rating/',views.AddStarRating.as_view(),name = "add_rating"),
    # path('<slug:slug>/',views.BookDetailView.as_view(), name = 'book_detail'),
    # path('<slug:slug>/<int:page_id>/',views.Page.as_view(), name = 'page'),
    # path('ajax/show_more_books/<int:page>/',views.ShowMoreBooks.as_view(), name = 'show_more_books'),
]