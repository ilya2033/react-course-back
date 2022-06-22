from django.db import models
from goods.models import Good
import uuid




class Category(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name', max_length = 200)
    parent =models.ForeignKey('self',default=None,null=True,blank=True,related_name = "subcategories", on_delete = models.CASCADE)
    goods = models.ManyToManyField(Good,related_name ="categories", blank = True)

