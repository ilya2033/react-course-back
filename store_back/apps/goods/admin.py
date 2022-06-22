from django.contrib import admin
from .models import Good, Image

@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
