from django.db import models
import uuid
from django.utils import timezone




class Image(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.ImageField(upload_to ='uploads/')



class Good(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name', max_length = 200)
    description = models.CharField('description', max_length = 1000)
    price = models.IntegerField("price", default=0)
    amount = models.IntegerField("amount", default=0)
    images = models.ManyToManyField(Image,related_name ="goods", blank = True)
    date = models.DateTimeField(default=timezone.now)

