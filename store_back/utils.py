from datetime import datetime
from graphql_jwt.settings import jwt_settings
from store_back.settings import GRAPHQL_JWT
from calendar import timegm

## JWT payload for Hasura
def jwt_payload(user, context=None):

    username = user.get_username()



    exp = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA

    payload = {
        user.USERNAME_FIELD: username,
        "exp": timegm(exp.utctimetuple()),
    }



    payload['iat'] =timegm(datetime.utcnow().utctimetuple())
    payload["sub"] = {
        "acl":["anon"],
    }

    if user._id:
        payload["sub"]["acl"].append(str(user._id))
        payload["sub"]["acl"].append("user")
        if  user.is_superuser:
            payload["sub"]["acl"].append("admin")
        payload["sub"]["login"] = user.username
        payload["sub"]["_id"] = str(user._id)


    return payload