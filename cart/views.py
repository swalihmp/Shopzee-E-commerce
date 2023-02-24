from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from accounts.models import Account,Address,UserProfile
from cart.models import Cart , Wishlist
from store.models import Product
from adminp.models import Coupon
from datetime import datetime
from django.urls import reverse
from store.views import singleproduct
import json
from django.utils import timezone

# from geopy.geocoders import Nominatim

# Create your views here.

def cart(request):
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
           
    context={
        'items':items,
        'item_count':item_count,
        'total':total,
        'witems':witems,
        'witem_count':witem_count,
    }
    return render(request,'cart.html',context)

def wishlist(request):
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
    
    context={
        'items':items,
        'item_count':item_count,
        'total':total,
        'witems':witems,
        'witem_count':witem_count,
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
    
def removewish(request,id):
    wishItem=Wishlist.objects.get(id=id)
    wishItem.delete()
    return redirect('wishlist') 


def addtocart(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            color = request.POST['color']
            size = request.POST['size']
            product = Product.objects.get(id=id)
            stock = product.stock
            user = request.user
            uid = user.username 
        
            if Cart.objects.filter(product=product,user=uid,color=color,size=size).exists():
                return redirect('cart')
            else:
                Cart.objects.create(product=product,user=uid,color=color,size=size)
                return redirect('cart')
    else:
        return redirect('login')
    
def cartinc(request):
    body = json.loads(request.body)
    qty=Cart.objects.get(id=body['id'])
    
    prod = qty.product
    if prod.stock > qty.quantity :
        qty.quantity += 1
        qty.save()
        str = "true"
        quantity = qty.quantity
        
        user = request.user
        user_name = user.username
        items=Cart.objects.filter(user=user_name)
        
        pname = qty.product.product_name
        product = Product.objects.get(product_name=pname)    
        sub_total = qty.quantity * product.price
        
        
        
        total =0
        for i in range(len(items)):
            x = items[i].product.price*items[i].quantity
            total = total+x
        
        
        data = {
            'total':total,
            'data': str,
            'quantity': quantity,
            'sub_total':sub_total
        }
        # return redirect('cart') 
        return JsonResponse(data)
    else:
        
        data = {
            'stock' : False
        }
        return JsonResponse(data)
    

def cartdic(request):
    body = json.loads(request.body)
    qty=Cart.objects.get(id=body['id'])
    qty.quantity -= 1
    qty.save()
    if qty.quantity == 0:
        qty.delete()
    str = "true"
    quantity = qty.quantity
    
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    
    pname = qty.product.product_name
    product = Product.objects.get(product_name=pname)    
    sub_total = qty.quantity * product.price
    
    total =0
    for i in range(len(items)):
        x = items[i].product.price*items[i].quantity
        total = total+x
        

    data = {
        'total':total,
        'data': str,
        'quantity': quantity,
        'sub_total': sub_total
    }
    # return redirect('cart') 
    return JsonResponse(data)   

def addressload(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        qty=Address.objects.get(id=body['id'])
        
        address_line_1 = qty.address_line_1
        address_line_2 = qty.address_line_2 
        name = qty.name
        city = qty.city
        state = qty.state
        country = qty.country
        zip_code = qty.zip_code
        phone = qty.phone
        
        data = {
            'address_line_1' : address_line_1,
            'address_line_2' : address_line_2,
            'name' : name,
            'city' : city ,
            'state' : state ,
            'country' : country ,
            'zip_code' : zip_code ,
            'phone' : phone 
        }
        
        return JsonResponse(data)


def remove(request,id):
    cartItem=Cart.objects.get(id=id)
    cartItem.delete()
    return redirect('cart') 

def checkout(request):
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
    
    profile = UserProfile.objects.get(user=user)
    addresses = Address.objects.filter(profile=profile)
    
    context={
        'items':items,
        'item_count':item_count,
        'total':total,
        'witems':witems,
        'witem_count':witem_count,
        'addresses':addresses,
    }
    return render(request,'checkout.html',context)

def apply_coupon(request):
    body = json.loads(request.body)
    
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    total =0
    for i in range(len(items)):
        x = items[i].product.price*items[i].quantity
        total = total+x
    
    coupon_id = body['coupon']
    
    try:
        coupon = Coupon.objects.get(coupon_id=coupon_id)
    
    except Coupon.DoesNotExist:
        data ={
            'coupon_id' : "Coupon Does Not Exist...",
            'g_total': total,
            'amount': "0",
            'coupon_name': ""
        }
        return JsonResponse(data)
    else : 
        date = datetime.now().date()
        sdate = coupon.activ_date
        edate = coupon.exp_date
        minimum = coupon.min_amount
        users = coupon.allowed_users
        if ( int(minimum)<int(total) and sdate <= date <= edate and users>0):
            
            amount = coupon.disc_amount
            coupon_id = coupon.coupon_id
            g_total = int(total)-int(amount)
            print(g_total)
            data ={
                'amount':amount,
                'coupon_id': coupon_id,
                'g_total': g_total,
                'coupon_name': coupon_id
            }
            return JsonResponse(data)
        else:
            amount = 0
            data ={
                'coupon_id' : "Minimal Cart Value",
                'g_total': total,
                'amount': amount,
                'coupon_name':coupon_id
            }
            return JsonResponse(data)