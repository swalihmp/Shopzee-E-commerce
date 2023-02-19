from django.db import models
from accounts.models import Account
from store.models import Product,Variation

# Create your models here.    
    
class Cart(models.Model):
    quantity=models.IntegerField(default=1)
    user=models.CharField(max_length=100,null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.CharField(max_length=30,blank=True)
    size = models.CharField(max_length=30,null=True)    
    
class Wishlist(models.Model):
    user=models.CharField(max_length=100,null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)