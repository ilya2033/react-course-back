import graphene
from graphene_django.types import DjangoObjectType
from .models import Category
import json
from functools import reduce
from .serializers import CategorySerializer
import operator
from django.db.models import Q
import goods.schema as  good_schema
from django.forms.models import model_to_dict




class CategoryType(graphene.ObjectType):
    _id = graphene.String(name='_id')
    name = graphene.String()
    parent = graphene.Field(lambda: CategoryType)
    goods = graphene.List(good_schema.GoodType)
    subcategories = graphene.List(lambda: CategoryType)

    def resolve__id(self,info):
        if isinstance(self, Category):
            return self._id
        else:
            return self

    def resolve_goods(self,info):
        try:
            iter(self.goods)
            return self.goods
        except:
            return self.goods.all()


    def resolve_parent(self,info):
        return self.parent


    def resolve_subcategories(self,info):
        query_set = []
        query_set = Category.objects.filter(parent = self._id)
        return query_set


class CategoryInput(graphene.InputObjectType):
    _id = graphene.String(name='_id')
    name = graphene.String()
    parent = graphene.Field(lambda:CategoryInput)
    goods = graphene.List(good_schema.GoodInput)
    subcategories = graphene.List(lambda:CategoryInput)



class Query(graphene.ObjectType):
    CategoryFind = graphene.List(CategoryType,query = graphene.String())
    CategoryFindOne = graphene.Field(CategoryType,query = graphene.String())


    def resolve_CategoryFind(self,info,query = "[{}]"):

        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")

        query_set = Category.objects.all()

        if len(filter_params):
            query_set = query_set.filter(reduce(operator.or_,(Q(**d) for d in [dict([i]) for i in filter_params.items()])))

        query_set = query_set.order_by(order_by)[skip:skip+limit]
        return query_set


    def resolve_CategoryFindOne(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")

        query_set = Category.objects.all()

        if len(filter_params):
            query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in filter_params.items()])))

        return query_set.first()




class CategoryUpsert(graphene.Mutation):

    class Arguments:
        category = CategoryInput(required=True)

    Output =CategoryType

    @staticmethod
    def mutate(root,info,category ={}):
        new_category={}
        good_list = []
        subcategories_list = []

        user = info.context.user
        if not user.is_superuser:
            raise Exception("Authentication credentials were not provided")


        if "goods" in category:
            good_list = [f['_id'] for f in category["goods"]]
            category.pop("goods",None)

        if "subcategories" in category:
            subcategories_list = [Category.objects.get(_id = f["_id"]) for f in category["subcategories"]]
            category.pop("subcategories",None)

        try:
            _id = category._id
            new_category = Category.objects.get(_id = _id)
            new_category.__dict__.update(**category)
        except Exception as e:

            new_category = Category(**category)
            
        
        if "parent" in category:
            try:
                if category.get("parent",None) == "null":
                    new_category.parent = None
                    
                new_category.parent = Category.objects.get(_id=category.get("parent",None)["_id"])
            except:
                raise Exception("Невірні дані (parent)")

        new_category.save()
        if len(good_list):
            new_category.goods.set(good_list)

        if len(subcategories_list):
            new_category.subcategories.set(subcategories_list)

        category_data = model_to_dict(new_category)
        category_data["_id"] = new_category._id
        return CategoryType(**category_data)




class CategoryDelete(graphene.Mutation):

    class Arguments:
        category =  CategoryInput(required=True)

    Output =CategoryType

    @staticmethod
    def mutate(root,info,category):
        user = info.context.user
        if not user.is_superuser:
            raise Exception("Authentication credentials were not provided")



        try:
            _id = category._id
            category_to_delete = Category.objects.get(_id=_id)
            category_data = model_to_dict(category_to_delete)
            category_data["_id"] = category_to_delete._id
            category_to_delete.delete()

        except:
            raise Exception("Не вірні дані")



        return CategoryType(**category_data)







class Mutations(graphene.ObjectType):

    CategoryUpsert = CategoryUpsert.Field()
    CategoryDelete = CategoryDelete.Field()



