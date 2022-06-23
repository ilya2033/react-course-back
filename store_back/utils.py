from datetime import datetime
from graphql_jwt.settings import jwt_settings
from store_back.settings import GRAPHQL_JWT

## JWT payload for Hasura
def jwt_payload(user, context=None):
    token = {}
    jwt_datetime = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA
    jwt_expires = int(jwt_datetime.timestamp())
    token['username'] = str(user.username) # For library compatibility
    token['exp'] = jwt_expires

    token['iat'] = datetime.timestamp(datetime.now())
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