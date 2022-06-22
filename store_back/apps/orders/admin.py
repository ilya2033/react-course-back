from django.contrib import admin
from .models import Order, OrderGood

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderGood)
class OrderGoodAdmin(admin.ModelAdmin):
    pass
