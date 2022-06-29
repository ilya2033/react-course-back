import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from goods.schema import ImageType,ImageInput
import json
from functools import reduce
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

import operator
from django.db.models import Q


User = get_user_model()


class UserType(graphene.ObjectType):
    _id = graphene.String(name='_id')
    avatar = graphene.Field(ImageType)
    name = graphene.String()
    nick = graphene.String()
    username = graphene.String()
    acl = graphene.List(graphene.String)
    createdAt = graphene.String()



    def resolve__id(self,info):
        return self._id

    def resolve_avatar(self,info):
        return self.avatar

    def resolve_nick(self,info):
        return self.nick

    def resolve_name(self,info):
        return self.name

    def resolve_username(self,info):
        return self.username

    def resolve_acl(self,info):
        print(self._id)
        user = User.objects.get(_id = self._id)
        print(user)
        acl = ["anon"]
        if user._id:
            acl.append(str(user._id))
            acl.append("user")
            if  user.is_superuser:
                acl.append("admin")

        print(acl)
        return acl


    def resolve_createdAt(self,info):
        return self.createdAt.strftime('%s')


class UserInput(graphene.InputObjectType):
    _id = graphene.String(name='_id')
    avatar = graphene.Field(ImageInput)
    name = graphene.String()
    nick = graphene.String()
    acl = graphene.List(graphene.String)
    username = graphene.String()





class Query(graphene.ObjectType):
    UserFind = graphene.List(UserType,query = graphene.String())
    UserFindOne = graphene.Field(UserType,query = graphene.String())

    # ImageFind = graphene.List(ImageType,query = graphene.String())
    # ImageFindOne = graphene.Field(ImageType,query = graphene.String())

    def resolve_UserFind(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = int(additional_params.get("skip",0))
        limit = int(additional_params.get("limit",20))
        order_by = additional_params.get("orderBy","_id")

        query_set = User.objects.all()


        if len(filter_params):
            query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in filter_params.items()])))

        query_set = query_set.order_by(order_by)[skip:skip+limit]
        return query_set


    def resolve_UserFindOne(self,info,query = "[{}]"):
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")

        query_set = User.objects.all()

        if len(filter_params):
            query_set = query_set.filter(reduce(operator.and_,(Q(**d) for d in [dict([i]) for i in filter_params.items()])))

        return query_set.first()






class UserUpsert(graphene.Mutation):

    class Arguments:
        user = UserInput(required=True)

    Output =UserType

    @staticmethod
    def mutate(root,info,user):
        new_user={}

        try:
            _id = user._id
            new_user = User.objects.get(_id = _id)
            user.pop("_id",None)
            new_user.__dict__.update(**user)
        except Exception as e:
            try:
                User.objects.get(username = user.username)
                raise Exception("Username вже зайнятий")
            except:
                pass
            new_user = User(**user)

        new_user.save()
        user_data =  {key: new_user.__dict__[key] for key in  new_user.__dict__.keys() & {"username","_id","name","avatar","nick"}}
        user_data["_id"] = new_user._id


        return UserType(**user_data)




# class GoodDelete(graphene.Mutation):

#     class Arguments:
#         good = GoodInput(required=True)

#     Output =GoodType

#     @staticmethod
#     def mutate(root,info,good):
#         user = info.context.user
#         if not user.is_superuser:
#             raise Exception("Authentication credentials were not provided")


#         try:
#             _id = good._id
#             good_to_delete = Good.objects.get(_id=_id)
#             good_data = model_to_dict(good_to_delete)
#             good_data["_id"] = new_good._id
#             good_to_delete.delete()
#         except:
#             raise Exception("Не вірні дані")



#         return GoodType(**good_data)







class Mutations(graphene.ObjectType):

    UserUpsert =  UserUpsert.Field()
    # GoodDelete = GoodDelete.Field()



