
from rest_framework import serializers
from .models import Good, Image
from categories.models import Category


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Category
        fields = ['_id','name']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Image
        fields = ['_id','url']



class GoodSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    categories =  SubCategorySerializer(many=True)
    class Meta:
        model =  Good
        fields = ['_id',"name","price","amount","description","images","categories"]
        depth = 1


