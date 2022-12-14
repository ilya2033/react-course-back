import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import Good,Image
import json
from functools import reduce
from .serializers import GoodSerializer
from django.forms.models import model_to_dict
from django.db.models import Count
from django.conf import settings

import operator
from django.db.models import Q



class ImageType(graphene.ObjectType):
    _id = graphene.String(name='_id')
    url = graphene.String()

    def resolve__id(self,info):
        return self._id

    def resolve_url(self,info):
        return settings.MEDIA_URL + str(self.url)


class ImageInput(graphene.InputObjectType):
    _id = graphene.String(name='_id')
    url = graphene.String(name='url')


class GoodType(graphene.ObjectType):
    _id = graphene.String(name='_id')
    images = graphene.List(ImageType)
    name = graphene.String()
    description = graphene.String()
    price = graphene.Int()
    amount = graphene.Int()
    categories = graphene.List('categories.schema.CategoryType')
    createdAt = graphene.String()



    def resolve__id(self,info):
        return self._id

    def resolve_images(self,info):
        return self.images.all().order_by("goodimage__order")

    def resolve_categories(self,info):
        return self.categories.all()

    def resolve_name(self,info):
        return self.name

    def resolve_description(self,info):
        return self.description

    def resolve_price(self,info):
        return self.price

    def resolve_amount(self,info):
        return self.amount

    def resolve_createdAt(self,info):
        return self.createdAt.strftime('%s')

class GoodInput(graphene.InputObjectType):
    _id = graphene.String(name='_id')
    images = graphene.List(ImageInput)
    name = graphene.String()
    description = graphene.String()
    price = graphene.Int()
    amount = graphene.Int()
    categories = graphene.List('categories.schema.CategoryInput')





class Query(graphene.ObjectType):
    GoodFind = graphene.List(GoodType,query = graphene.String())
    GoodFindOne = graphene.Field(GoodType,query = graphene.String())

    ImageFind = graphene.List(ImageType,query = graphene.String())
    ImageFindOne = graphene.Field(ImageType,query = graphene.String())

    def resolve_GoodFind(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = int(additional_params.get("skip",0))
        limit = int(additional_params.get("limit",20))
        order_by = additional_params.get("orderBy","_id")

        query_set = Good.objects.all()


        if len(filter_params):
            or_filter_params = filter_params.pop("or",{})
            and_filter_params= filter_params.pop("and",{})
            and_filter_params |= filter_params
            if len(or_filter_params):
                query_set = query_set.filter(reduce(operator.or_,(Q(**d) for d in [dict([i]) for i in or_filter_params.items()])))
            if len(and_filter_params):
                query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in and_filter_params.items()])))
                
        if order_by == 'popular':
            query_set = query_set.annotate(order_count=Count('orderGoods')).order_by("-order_count")[skip:skip+limit]
        else:
            query_set = query_set.order_by(order_by)[skip:skip+limit]

        return query_set


    def resolve_GoodFindOne(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")

        query_set = Good.objects.all()

        if len(filter_params):
            or_filter_params = filter_params.pop("or",{})
            and_filter_params= filter_params.pop("and",{})
            and_filter_params |= filter_params
            if len(or_filter_params):
                query_set = query_set.filter(reduce(operator.or_,(Q(**d) for d in [dict([i]) for i in or_filter_params.items()])))
            if len(and_filter_params):
                query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in and_filter_params.items()])))
                
        return query_set.first()



    def resolve_ImageFind(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")

        query_set = Image.objects.all()

        if len(filter_params):
            or_filter_params = filter_params.pop("or",{})
            and_filter_params= filter_params.pop("and",{})
            and_filter_params |= filter_params
            if len(or_filter_params):
                query_set = query_set.filter(reduce(operator.or_,(Q(**d) for d in [dict([i]) for i in or_filter_params.items()])))
            if len(and_filter_params):
                query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in and_filter_params.items()])))
                

        return query_set


    def resolve_ImageFindOne(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")

        query_set = Image.objects.all()

        if len(filter_params):
            try:
                or_filter_params = filter_params.pop("or",{})
                and_filter_params= filter_params.pop("and",{})
                and_filter_params |= filter_params
                if len(or_filter_params):
                    query_set = query_set.filter(reduce(operator.or_,(Q(**d) for d in [dict([i]) for i in or_filter_params.items()])))
                if len(and_filter_params):
                    query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in and_filter_params.items()])))
            except:
                raise Exception("???? ?????????? ????????")
        return query_set.first()




class GoodUpsert(graphene.Mutation):

    class Arguments:
        good = GoodInput(required=True)

    Output =GoodType

    @staticmethod
    def mutate(root,info,good):
        new_good={}
        image_list = None
        category_list = None

        user = info.context.user
        if not user.is_superuser:
            raise Exception("Authentication credentials were not provided")

        if "images" in good:
            image_list = [f["_id"] for f in good["images"]]
        #     image_list = []
        #     for idx, image in enumerate(good["images"]):
        #         image["order"] = idx+1
        #         image_list.append(image)



            good.pop("images",None)


        if "categories" in good:
            category_list = [f['_id'] for f in good["categories"]]
            good.pop("categories",None)

        try:
            _id = good._id
            new_good = Good.objects.get(_id = _id)
            good.pop("_id",None)
            new_good.__dict__.update(**good)
        except Exception as e:
            new_good = Good(**good)

        new_good.save()

        if image_list != None:
            new_good.images.set(image_list)
            
            for idx,image in enumerate(image_list):
                instance = new_good.GoodImages.get(image = image)
                instance.order = idx+1
                instance.save()
        
        if category_list != None:
            new_good.categories.set(category_list)    

        new_good.save()
        good_data = model_to_dict(new_good)
        good_data["_id"] = new_good._id
        return GoodType(**good_data)




class GoodDelete(graphene.Mutation):

    class Arguments:
        good = GoodInput(required=True)

    Output =GoodType

    @staticmethod
    def mutate(root,info,good):
        user = info.context.user

        if not user.is_superuser:
            raise Exception("Authentication credentials were not provided")


        try:
            _id = good._id
            good_to_delete = Good.objects.get(_id=_id)
            good_data = model_to_dict(good_to_delete)
            good_data["_id"] = good_to_delete ._id
            good_to_delete.delete()
        except:
            raise Exception("???? ?????????? ????????")



        return GoodType(**good_data)







class Mutations(graphene.ObjectType):

    GoodUpsert = GoodUpsert.Field()
    GoodDelete = GoodDelete.Field()



