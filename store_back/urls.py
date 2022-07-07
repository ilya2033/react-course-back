
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from .schema import schema
from goods.views import image_upsert


urlpatterns = [
    path('api/', include('goods.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('categories.urls')),
    path('api/upload/',image_upsert),
    path('api/auth/',include('authAPI.urls')),
    path('api/admin/', admin.site.urls),
    path('api/graphql/',csrf_exempt(GraphQLView.as_view(
        graphiql=True,
        schema = schema
    )))

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)