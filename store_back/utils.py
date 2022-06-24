from datetime import datetime
from graphql_jwt.settings import jwt_settings
from store_back.settings import GRAPHQL_JWT

## JWT payload for Hasura
def jwt_payload(user, context=None):
    token = {}

    token['iat'] =str(datetime.timestamp(datetime.now()))
    token["sub"] = {
        "acl":["anon"],
    }
    if user._id:
        token["sub"]["acl"].append(str(user._id))
        if  user.is_superuser:
            token["sub"]["acl"].append("admin")
        token["sub"]["login"] = user.username
        token["sub"]["_id"] = str(user._id)
    return token