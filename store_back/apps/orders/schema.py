import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import Order,OrderGood
from goods.models import Good
import json
from authAPI.schema import UserInput
from functools import reduce
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

import operator
from django.db.models import Q


User = get_user_model()



class OrderGoodType(graphene.ObjectType):
    _id = graphene.String(name='_id')
    good = graphene.Field('goods.schema.GoodType')
    price = graphene.Int()
    count = graphene.Int()
    order = graphene.Field(lambda:OrderType)
    createdAt = graphene.String()

    def resolve__id(self,info):
        return self._id

    def resolve_good(self,info):
        return self.good

    def resolve_price(self,info):
        return self.price

    def resolve_count(self,info):
        return self.count

    def resolve_order(self,info):
        return self.order



    def resolve_createdAt(self,info):
        return self.createdAt.strftime('%s')


class OrderGoodInput(graphene.InputObjectType):
    _id = graphene.String(name='_id')
    good = graphene.Field("goods.schema.GoodInput")
    count = graphene.Int()







class OrderType(graphene.ObjectType):
    _id = graphene.String(name='_id')
    createdAt = graphene.String()
    status = graphene.Int()
    price = graphene.Int()
    orderGoods = graphene.List(OrderGoodType)
    delivery = graphene.String()
    owner = graphene.Field('authAPI.schema.UserType')



    def resolve__id(self,info):
        return self._id

    def resolve_status(self,info):
        return self.status

    def resolve_price(self,info):
        return self.price

    def resolve_delivery(self,info):
        return self.delivery

    def resolve_orderGoods(self,info):
        try:
            iter(self.orderGoods)
            return self.orderGoods
        except:
            return self.orderGoods.all()

    def resolve_owner(self,info):
        return self.owner

    def resolve_createdAt(self,info):
        return self.createdAt.strftime('%s')


class OrderInput(graphene.InputObjectType):
    _id = graphene.String(name='_id')
    status = graphene.Int()
    price = graphene.Int()
    delivery = graphene.String()
    owner = graphene.Field(UserInput)
    orderGoods = graphene.List(OrderGoodInput)






class Query(graphene.ObjectType):
    OrderFind = graphene.List(OrderType,query = graphene.String())
    OrderFindOne = graphene.Field(OrderType,query = graphene.String())

    OrderGoodFind = graphene.List(OrderGoodType,query = graphene.String())
    OrderGoodFindOne = graphene.Field(OrderGoodType,query = graphene.String())

    def resolve_OrderFind(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
  
        if "status" in filter_params and int(filter_params.get("status")) == 0:
            filter_params.pop("status")
            
        if len(query_list) > 1:
            additional_params = query_list[1]


        skip = int(additional_params.get("skip",0))
        limit = int(additional_params.get("limit",20))
        order_by = additional_params.get("orderBy","_id")

        user = info.context.user
        if user.is_superuser:
            query_set = Order.objects.all()
        else:
            query_set = Order.objects.filter(owner = user)


        if len(filter_params):
            query_set = query_set.filter(reduce(operator.or_,(Q(**d) for d in [dict([i]) for i in filter_params.items()])))

        query_set = query_set.order_by(order_by)[skip:skip+limit]
        return query_set


    def resolve_OrderFindOne(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")
        user = info.context.user

        if  user.is_superuser:
            query_set = Order.objects.all()
        else:
            query_set = Order.objects.filter(owner = user)

        if len(filter_params):
            query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in filter_params.items()])))

        return query_set.first()



    def resolve_OrderGoodFind(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")

        query_set = OrderGood.objects.all()

        if len(filter_params):
            query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in filter_params.items()])))


        return query_set


    def resolve_OrderGoodFindOne(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")

        query_set = OrderGood.objects.all()

        if len(filter_params):
            query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in filter_params.items()])))

        return query_set.first()




class OrderUpsert(graphene.Mutation):

    class Arguments:
        order = OrderInput(required=True)

    Output =OrderType

    @staticmethod
    def mutate(root,info,order):

        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")

        orderPrice = 0
        new_order={}
        owner = None
        orderGoods_list = []


        if "orderGoods" in order:
            orderGoods_list = order.pop("orderGoods",[])

        
        if "owner" in order:
            try:
                owner = User.objects.get(pk =order.pop("owner")["_id"])
            except:
                raise Exception("Не вірні дані")

        try:
            if "_id" in order:

                new_order = Order.objects.get(_id = order._id)

                if not user.is_superuser:
                    raise Exception("Authentication credentials were not provided")

                new_order.__dict__.update(**order)

                if owner:
                    new_order.owner = owner

            else:
                new_order = Order(**order)
                new_order.owner = user

        except Exception as e:
            raise Exception("Не вірні дані")


        if new_order:
            new_order.save()

        for orderGood in new_order.orderGoods.all():
            if new_order.status != 4:
                orderGood.good.amount += orderGood.count
                orderGood.good.save()

        new_order.orderGoods.clear()
        for orderGood in orderGoods_list:

            try:
                good = Good.objects.get(_id = orderGood.get("good")["_id"])
            except:
                raise Exception("Товар не знайдено")

            count = orderGood.get("count")
            if int(good.amount) - int(count) >= 0:
                price = int(count) * int(good.price)
                orderGoodToSave = OrderGood.objects.create(price = price, count = count, good = good)
                orderGoodToSave.save()
                new_order.orderGoods.add(orderGoodToSave)
                orderPrice+=int(price)

                if int(new_order.status) != 4:
                    good.amount = int(good.amount) - int(count)
                    good.save()

            else:
                raise Exception(f"{good.name}:Недостатньо товару!")

        new_order.price = orderPrice


        if new_order:
            new_order.save()

        else:
            raise Exception("Error during order save")



        order_data = model_to_dict(new_order)
        order_data["_id"] = new_order._id
        order_data["orderGoods"] = new_order.orderGoods.all()

        return OrderType(**order_data)


class OrderDelete(graphene.Mutation):

    class Arguments:
        order = OrderInput(required=True)

    Output =OrderType

    @staticmethod
    def mutate(root,info,order):
        user = info.context.user
        if not user.is_superuser:
            raise Exception("Authentication credentials were not provided")


        try:
            _id = order._id
            order_to_delete = Order.objects.get(_id=_id)
            order_data = model_to_dict(order_to_delete)
            order_data["_id"] = order_to_delete._id
            order_data["orderGoods"] = order_to_delete.orderGoods.all()
            order_to_delete.delete()

        except:
            raise Exception("Не вірні дані")



        return OrderType(**order_data)







class Mutations(graphene.ObjectType):

    OrderUpsert = OrderUpsert.Field()
    OrderDelete = OrderDelete.Field()



