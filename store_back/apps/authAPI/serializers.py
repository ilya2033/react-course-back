from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['iat'] = str(datetime.timestamp(datetime.now()))
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