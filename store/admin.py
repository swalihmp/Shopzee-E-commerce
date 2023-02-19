from django.contrib import admin
from .models import Product,Variation,multiimages,Review_Rating

from django.utils.html import format_html

# Register your models here.

class MultiImagesAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="40" style="border-radius:50%;">'.format(object.image.url))
    thumbnail.short_discription='product picture'
    list_display=('thumbnail','product')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'stock', 'category','is_available','price')
    prepopulated_fields = {'slug':['product_name',]}
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value','is_active')

admin.site.register(Product,ProductAdmin)

admin.site.register(Variation,VariationAdmin)
admin.site.register(multiimages,MultiImagesAdmin)

admin.site.register(Review_Rating)