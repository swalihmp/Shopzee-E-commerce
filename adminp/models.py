from django.db import models

# Create your models here.


class Slider(models.Model):
    image = models.ImageField(upload_to='photos/slider')
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    
