import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from goods.schema import ImageType,ImageInput
import json
from functools import reduce
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from goods.models import Image

import operator
from django.db.models import Q

import graphene
import graphql_jwt

User = get_user_model()


class UserType(graphene.ObjectType):
    _id = graphene.String(name='_id')
    avatar = graphene.Field(ImageType)
    name = graphene.String()
    nick = graphene.String()
    username = graphene.String()
    acl = graphene.List(graphene.String)
    is_active = graphene.Boolean(name = 'is_active')
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


    def resolve_is_active(self,info):
        return self.is_active


    def resolve_acl(self,info):
        user = User.objects.get(_id = self._id)
        acl = ["anon"]
        if user._id:
            if user.is_active:
                acl.append("active")
            if  user.is_superuser:
                acl.append("admin")

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
    password = graphene.String()





class Query(graphene.ObjectType):
    UserFind = graphene.List(UserType,query = graphene.String())
    UserFindOne = graphene.Field(UserType,query = graphene.String())



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
            query_set = query_set.filter(reduce(operator.or_,(Q(**d) for d in [dict([i]) for i in filter_params.items()])))

        print(query_set)
        query_set = query_set.order_by(order_by)[skip:skip+limit]
        return query_set


    def resolve_UserFindOne(self,info,query = "[{}]"):
        user = info.context.user
        additional_params = {}
        query_list = json.loads(query)
        filter_params = query_list[0]
        if len(query_list) > 1:
            additional_params = query_list[1]

        skip = additional_params.get("skip",0)
        limit = additional_params.get("limit",20)
        order_by = additional_params.get("orderBy","_id")

        if user.is_superuser:
            query_set = User.objects.all()
        else:
            query_set = User.objects.filter(pk=user._id)



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
        password = None
        ava = None
        acl = []

        if "password" in user and len(user["password"]) < 3:
            raise Exception("Не вірні дані (пароль)")
        elif "password" in user:
            password = str(user.pop("password"))

        if "acl" in user:
            acl = user.get("acl", [])
            user.pop("acl")

        if "avatar" in user:
            if user.get("avatar") == "null":
                ava = user.pop("avatar")
            else:
                try:
                    ava = Image.objects.get(_id = user.pop("avatar")["_id"])
                except:
                    raise Exception("Не вірні дані (аватар)")

        try:
            _id = user._id
            new_user = User.objects.get(_id = _id)
            if not info.context.user.is_superuser:
                raise Exception("Authentication credentials were not provided")

            user.pop("_id",None)
            new_user.__dict__.update(**user)

            if password:
                new_user.set_password(password)
    

        except Exception as e:

            if info.context.user.is_authenticated:
                try:
                    new_user = User.objects.get(username = info.context.user.username)
                    new_user.__dict__.update(**user)
                    if password:
                        new_user.set_password(password)
                except:
                    raise Exception("Не вірні дані")
            else:
                try:
                    User.objects.get(username = user.username)
                    raise Exception("Username вже зайнятий")
                except:
                    pass

                new_user = User.objects.create_user(username = user.username,password=user.password)

        if ava:
            if ava == "null":
                new_user.avatar = None

            else:
                new_user.avatar = ava


        if len(acl):
            if not info.context.user.is_superuser:
                raise Exception("Authentication credentials were not provided")
            
            new_user.is_active = "active" in acl
            new_user.is_superuser = "admin" in acl

        new_user.save()




        user_data =  {key: new_user.__dict__[key] for key in  new_user.__dict__.keys() & {"username","_id","name","avatar","nick"}}
        user_data["_id"] = new_user._id


        return UserType(**user_data)









class Mutations(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


    UserUpsert =  UserUpsert.Field()



