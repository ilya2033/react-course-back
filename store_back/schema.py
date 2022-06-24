import graphene
from goods.schema import Query as good_query
from categories.schema import Query as category_query
from goods.schema import Mutations as good_mutations
from categories.schema import Mutations as category_mutations

import graphql_jwt


class Mutation(good_mutations,category_mutations):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()


class Query(good_query,category_query):
    pass


schema = graphene.Schema(query = Query,mutation=Mutation)