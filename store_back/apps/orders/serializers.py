
from rest_framework import serializers
from .models import Order,OrderGood
from goods.serializers import GoodSerializer




class OrderGoodSertializer(serializers.ModelSerializer):
    good = GoodSerializer()
    class Meta:
        model =  OrderGood
        fields = ['_id',"price","count","good",]


class OrderSerializer(serializers.ModelSerializer):
    orderGoods = OrderGoodSertializer(many=True)
    class Meta:
        model =  Order
        fields = ['_id',"date","price","status","orderGoods","phoneNumber","email","name","surname","address","delivery"]


