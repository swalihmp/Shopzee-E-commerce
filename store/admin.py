from django.contrib import admin
from .models import Product,Variation

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'stock', 'category','is_available','price')
    prepopulated_fields = {'slug':['product_name',]}
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value','is_active')

admin.site.register(Product,ProductAdmin)

admin.site.register(Variation,VariationAdmin)