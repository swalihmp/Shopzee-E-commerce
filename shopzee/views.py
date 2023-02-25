from django.shortcuts import render
from store.models import Product
from adminp.models import Slider
from cart.models import Cart , Wishlist

# Create your views here.

# def custom_404(request, exception=None):
#     return render(request, '404.html')


def HomePage(request):
    if request.user.is_authenticated:
        products = Product.objects.all().filter(is_available=True)
        slider = Slider.objects.all()
        user = request.user
        user_name = user.username
        items=Cart.objects.filter(user=user_name)
        item_count = items.count()
        
        witems=Wishlist.objects.filter(user=user_name)
        witem_count = witems.count()
        
        
        total =0
        for i in range(len(items)):
            x = items[i].product.price*items[i].quantity
            total = total+x
            
        context = {
            'item_count':item_count,
            'products':products,
            'slider':slider,
            'items':items,
            'total':total,
            'witem_count':witem_count,
            'witems':witems,
        }
        return render(request,'index.html',context)
    else:
        products = Product.objects.all().filter(is_available=True)
        slider = Slider.objects.all()
        user = request.user
        user_name = user.username
        items=Cart.objects.filter(user=user_name)
        item_count = items.count()
        
        witems=Wishlist.objects.filter(user=user_name)
        witem_count = witems.count()
        
        
        total =0
        for i in range(len(items)):
            x = items[i].product.price*items[i].quantity
            total = total+x
            
        context = {
            'item_count':item_count,
            'products':products,
            'slider':slider,
            'items':items,
            'total':total,
            'witem_count':witem_count,
            'witems':witems,
        }
        return render(request,'index.html',context)

def page404(request, exception):
    return render(request, '404.html', status=404)