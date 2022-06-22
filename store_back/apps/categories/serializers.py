
from rest_framework import serializers
from .models import Category
from goods.serializers import GoodSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Category
        fields = ['_id','name']

class CategorySerializer(serializers.ModelSerializer):
    parent = SubCategorySerializer()
    subcategories =SubCategorySerializer(many=True)
    goods = serializers.SerializerMethodField()

    def get_goods(self, instance):
        goods = instance.goods.all().order_by(self.context.get("goods_order_by","_id"))
        return GoodSerializer(goods, many=True).data

    class Meta:
        model =  Category
        fields = ['_id','name','parent','subcategories','goods']



