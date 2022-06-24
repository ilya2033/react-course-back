
from rest_framework import serializers
from .models import Category
from goods.serializers import GoodSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Category
        fields = ['_id','name']

class CategorySerializer(serializers.ModelSerializer):
    goods = GoodSerializer(many=True)


    class Meta:
        model =  Category
        fields = ['_id','name','parent','subcategories','goods']
        depth = 1


    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['subcategories'] = CategorySerializer(many=True)
        fields['parent'] = CategorySerializer()
        return fields

