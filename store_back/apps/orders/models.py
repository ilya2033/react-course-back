from django.db import models
from goods.models import Good
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid


class Order(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField(default=timezone.now)
    status = models.IntegerField("status", default=1)
    price = models.IntegerField("price", default=1)
    delivery = models.CharField("delivery",max_length=50,default="-")
    owner = models.ForeignKey(get_user_model(),related_name="orders",on_delete=models.SET_NULL, null = True)



class OrderGood(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    price = models.IntegerField("price", default=1)
    count = models.IntegerField("count", default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderGoods",blank=True,null=True)
    createdAt = models.DateTimeField(default=timezone.now)




