import graphene
from goods.schema import Query as good_query
from categories.schema import Query as category_query
from orders.schema import Query as order_query
from authAPI.schema import Query as auth_query
from goods.schema import Mutations as good_mutations
from categories.schema import Mutations as category_mutations
from orders.schema import Mutations as order_mutations
from authAPI.schema import Mutations as auth_mutations

import graphql_jwt


class Mutation(good_mutations,category_mutations,order_mutations,auth_mutations):
    pass


class Query(good_query,category_query,order_query,auth_query):
    pass


schema = graphene.Schema(query = Query,mutation=Mutation)