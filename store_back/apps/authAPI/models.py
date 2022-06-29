import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("name",max_length=50,default="-")
    nick = models.CharField("nick",max_length=50,default="-")
    avatar = models.ForeignKey('goods.Image', null = True, on_delete=models.CASCADE)
    login = models.CharField("login",max_length=50,default="-")

    def __str__(self):
        return self.username