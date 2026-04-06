from django.db import models
from common.models import BaseModel



class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class SubCategory(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='subcategories')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')

    def __str__(self):
        return self.name