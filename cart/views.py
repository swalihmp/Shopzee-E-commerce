from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Account
from cart.models import Cart , Wishlist
from store.models import Product

# Create your views here.

def cart(request):
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name).order_by('id')
    item_count = items.count()
    
    total =0
    for i in range(len(items)):
        x = items[i].product.price*items[i].quantity
        total = total+x
        
        
    context={
        'items':items,
        'item_count':item_count,
        'total':total,
    }
    return render(request,'cart.html',context)

def wishlist(request):
    user = request.user
    uid = user.username
    items=Wishlist.objects.filter(user=uid).order_by('id')
    item_count = items.count()
    
    context={
        'witems':items,
        'witem_count':item_count,
    }
    return render(request,'wishlist.html',context)

def addtowish(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        user = request.user
        uid = user.username
        
        if Wishlist.objects.filter(product=product,user=uid).exists():
            return redirect('wishlist')
        
        else:
            Wishlist.objects.create(product=product,user=uid)
            return redirect('wishlist')
    else:
        return redirect('login')


def addtocart(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        user = request.user
        uid = user.username 
    
        if Cart.objects.filter(product=product,user=uid).exists():
            return redirect('cart')
        else:
            Cart.objects.create(product=product,user=uid)
            
            return redirect('cart')
    else:
        return redirect('login')
    
def cartinc(request,id):
    qty=Cart.objects.get(id=id)
    qty.quantity += 1
    qty.save()
    return redirect('cart') 

def cartdic(request,id):
    qty=Cart.objects.get(id=id)
    qty.quantity -= 1
    qty.save()
    if qty.quantity == 0:
        qty.delete()
    return redirect('cart')   

def remove(request,id):
    cartItem=Cart.objects.get(id=id)
    cartItem.delete()
    return redirect('cart') 