from django.db import models
from goods.models import Good
from django.utils import timezone
import uuid


class Order(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField("status", default=1)
    price = models.IntegerField("price", default=1)
    phoneNumber = models.CharField("phoneNumber", max_length=15)
    delivery = models.CharField("delivery",max_length=50,default="-")
    address = models.CharField("address",max_length=150,default="-")
    name = models.CharField("name",max_length=150,default="-")
    surname = models.CharField("surname",max_length=150,default="-")
    email  = models.CharField("email", max_length=50)



class OrderGood(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    price = models.IntegerField("price", default=1)
    count = models.IntegerField("count", default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderGoods",blank=True,null=True)





