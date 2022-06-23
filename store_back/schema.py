import graphene
from goods.schema import Query as good_query
from goods.schema import Mutations as good_mutations

import graphql_jwt


class Mutation(good_mutations):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()


class Query(good_query):
    pass


schema = graphene.Schema(query = Query,mutation=Mutation)