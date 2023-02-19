from django.db import models
from store.models import Product

# Create your models here.


class Slider(models.Model):
    image = models.ImageField(upload_to='photos/slider')
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    
class Coupon(models.Model):
    coupon_id = models.CharField(max_length=100,null=False)
    min_amount = models.CharField(max_length=50,null=True)
    activ_date = models.DateField(null=True)
    exp_date = models.DateField(null=True)
    allowed_users = models.IntegerField()
    disc_amount = models.CharField(max_length=20,default=0)
    
    def __str__(self):
        return self.coupon_id
    
