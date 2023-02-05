from django.db import models
from accounts.models import Account
from store.models import Product

# Create your models here.    
    
class Cart(models.Model):
    quantity=models.IntegerField(default=1)
    user=models.CharField(max_length=100,null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    
class Wishlist(models.Model):
    user=models.CharField(max_length=100,null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)