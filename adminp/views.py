from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Account
from store.models import Product,Variation,VariationManager
from category.models import Category
from .models import Slider,Coupon
import datetime
from orders.models import Payment,Order,OrderProduct

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import os


def adminpanel(request):
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d")
    
    today_orders = Order.objects.filter(created_at = current_date)
    total_orders = Order.objects.filter(is_ordered=True)
    today_count = today_orders.count()
    total_count = total_orders.count()
    
    today_total =0
    for i in range(len(today_orders)):
        x = today_orders[i].order_total
        today_total = today_total+x
        
    all_total = 0
    for i in range(len(total_orders)):
        x = total_orders[i].order_total
        all_total = all_total+x
        
    all_total = format(all_total, '.3f')
    
    context = {
        'today_count' : today_count,
        'total_count' :total_count,
        'today_total' : today_total,
        'all_total' : all_total,
    }
    
    return render(request, 'admin/adminpanel.html',context)



def productvar(request):
    if request.method == 'POST':
        pname = request.POST['pname']
        product = Product.objects.get(product_name=pname)
        variation_category = request.POST['category']
        variation_value = request.POST['value']
        
        Variation.object.create(
            product = product,
            variation_category = variation_category,
            variation_value = variation_value,
        )
        products = Variation.object.all().order_by('id')
        paginator = Paginator(products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products = Product.objects.filter(is_available = True)
        

        context = {
            'variations': paged_products,
            'products': products,
        }
        return render(request, 'admin/prodvariation.html',context)
    else:
        products = Variation.object.all().order_by('id')
        paginator = Paginator(products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products = Product.objects.filter(is_available = True)
        

        context = {
            'variations': paged_products,
            'products': products,
        }
        return render(request, 'admin/prodvariation.html',context)




def productsingle(request,id):
    context = {
        'product': Product.objects.get(id=id),
    }
    return render(request, 'admin/productsingle.html',context)


def adminaddproduct(request):
    categories=Category.objects.all()
    if request.method == 'POST':
        product_name = request.POST['product_name']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        images = request.FILES['images']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        
        
        Product.objects.create(
            product_name=product_name,
            description=description,
            price=price,
            images=images,
            stock=stock,
            category=category,
        )
        
        Products=Product.objects.all().order_by('id')
        prod_count=Products.count()
        context={
            'Products':Products,
            'prod_count':prod_count,
        }
        return render(request, 'admin/adminproducts.html',context)
    else:
        context={
            'categories':categories
        }
        return render(request, 'admin/adminaddproduct.html',context)

def adminproducts(request):
    Products=Product.objects.all().order_by('id')
    prod_count=Products.count()
    context={
        'Products':Products,
        'prod_count':prod_count,
    }
    return render(request, 'admin/adminproducts.html',context)

def category(request):
    Categorys=Category.objects.all().order_by('id')
    Cat_count = Categorys.count()
    context={
        'Categorys':Categorys,
        'Cat_count':Cat_count,
    }
    return render(request, 'admin/category.html',context)

def users(request):
    Users=Account.objects.filter(is_admin = False).order_by('id')
    user_count=Users.count()
    context={
        'Users':Users,
        'user_count':user_count,
    }
    return render(request,'admin/users.html',context)

def orders(request):
    orders = Order.objects.all().order_by('id')
    context = {
        'orders':orders,
    }
    return render(request,'admin/orders.html',context)

def order_details(request,id):
    single_order = Order.objects.get(id=id)
    ordered_products = OrderProduct.objects.filter(order_id=single_order.id)
    
    context ={
        'single_order': single_order,
        'products':ordered_products,
    }
    return render(request,'admin/order_details.html',context)


def blockuser(request,id,action):
    user=Account.objects.get(id=id)
    if action=='block':
        user.is_active=False
        user.save()
    elif action =='unblock':
        user.is_active=True
        user.save()

    return redirect('users')


def change(request,id,action):
    order=Order.objects.get(id=id)
    if action=='packed':
        order.status="Packed"
        order.save()
    elif action =='shipped':
        order.status="Shipped"
        order.save()
    elif action =='deliverd':
        order.status="Delivered"
        order.save()

    return redirect('orders')

def blockvari(request,id,action):
    prod=Variation.object.get(id=id)
    if action=='block':
        prod.is_active=False
        prod.save()
    elif action =='unblock':
        prod.is_active=True
        prod.save()

    return redirect('productvar')


def unlist(request,id,action):
    product=Product.objects.get(id=id)
    if action=='block':
        product.is_available=False
        product.save()
    elif action =='unblock':
        product.is_available=True
        product.save()
        
    Products=Product.objects.all().order_by('id')
    prod_count=Products.count()
    context={
        'Products':Products,
        'prod_count':prod_count,
    }
    return render(request, 'admin/adminproducts.html',context)    
        
def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        description = request.POST['description']
        cat_image = request.FILES['cat_image']
        
        Category.objects.create(
            category_name = category_name,
            description = description,
            cat_image = cat_image,
        )
        Categorys=Category.objects.all().order_by('id')
        Cat_count = Categorys.count()
        context={
            'Categorys':Categorys,
            'Cat_count':Cat_count,
        }
        return render(request, 'admin/category.html',context)
    else:
        return render(request,'admin/addcategory.html')
    
def editcategory(request,id):
    if request.method == 'POST':
        single_cat = Category.objects.get(id=id)
        if not request.FILES.get('cat_image'):
            ex1 = Category.objects.filter(id=id).update(
                category_name = request.POST['category_name'],
                description = request.POST['description'],
            )
            return redirect('category')
        else:
            os.remove(single_cat.cat_image.path)
            single_cat.cat_image = request.FILES['cat_image']
            single_cat.save()
            ex1 = Category.objects.filter(id=id).update(
                category_name = request.POST['category_name'],
                description = request.POST['description'],
            )
            return redirect('category')
    else:
        context = {
            'category': Category.objects.get(id=id)
        }
        return render(request,'admin/editcategory.html',context)

def deleteslider(request,id):
    slide_data = Slider.objects.get(id=id)
    slide_data.delete()
    return redirect('slideshow')


        
        
def slideshow(request):
    slides = Slider.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        name = request.POST['name']
        image = request.FILES['image']
        
        Slider.objects.create(
            title = title,
            name = name,
            image = image,
        )
        context ={
            'slides' : slides,
        }  
        return render(request,'admin/slideshow.html',context)  
    else:
        context ={
            'slides' : Slider.objects.all()
        }  
        return render(request,'admin/slideshow.html',context)
    
 
def addcoupon(request):
    coupons = Coupon.objects.all()
    if request.method == 'POST':
        coupon_id = request.POST['coupon_id']
        min_amount = request.POST['min_amount']
        activ_date = request.POST['activ_date']
        exp_date = request.POST['exp_date']
        allowed_users = request.POST['allowed_users']
        disc_amount = request.POST['disc_amount']
        
        if Coupon.objects.filter(coupon_id=coupon_id).exists():
            context ={
                'coupons' : coupons,
            }  
            return render(request,'admin/addcoupon.html',context)
        else:
            Coupon.objects.create(
                coupon_id = coupon_id,
                min_amount = min_amount,
                activ_date = activ_date,
                exp_date = exp_date,
                allowed_users = allowed_users,
                disc_amount = disc_amount,
            )
            context ={
                'coupons' : coupons,
            }  
            return render(request,'admin/addcoupon.html',context) 
    else:
        context ={
            'coupons' : Coupon.objects.all()
        }  
        return render(request,'admin/addcoupon.html',context)   

def deletecoupon(request,id):
    coupon_data = Coupon.objects.get(id=id)
    coupon_data.delete()
    return redirect('addcoupon')       
