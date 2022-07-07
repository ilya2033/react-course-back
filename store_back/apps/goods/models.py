from django.db import models
import uuid
from django.utils import timezone



class Image(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.ImageField(upload_to ='uploads/')



class Good(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name',default="", max_length = 200,blank=True)
    description = models.CharField('description',default="", max_length = 1000,blank=True)
    price = models.IntegerField("price", default=0,blank=True)
    amount = models.IntegerField("amount", default=0,blank=True)
    images = models.ManyToManyField(Image,related_name ="goods", blank = True,through='GoodImage')
    createdAt = models.DateTimeField(default=timezone.now)



class GoodImage(models.Model):
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    good = models.ForeignKey(Good,on_delete=models.CASCADE,related_name="GoodImages")
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ('order',)