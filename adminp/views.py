from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from accounts.models import Account
from store.models import Product,Variation,VariationManager,multiimages
from category.models import Category
from .models import Slider,Coupon
import datetime
from datetime import timedelta
from orders.models import Payment,Order,OrderProduct

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import os



@login_required(login_url = 'login')
def adminpanel(request):
    if request.user.is_superadmin:
        current_date = datetime.datetime.now()
        date = current_date.date()
        
        today_orders = Order.objects.filter(created_at = date)
        today_count = today_orders.count()
        total_orders = Order.objects.filter(is_ordered=True)
        total_count = total_orders.count()
        
        today_total =0
        for i in range(len(today_orders)):
            x = today_orders[i].order_total
            today_total = today_total+x
        
        today_total = format(today_total, '.3f')        
            
        all_total = 0
        for i in range(len(total_orders)):
            x = total_orders[i].order_total
            all_total = all_total+x
            
        all_total = format(all_total, '.3f')
        orders = Order.objects.filter(is_ordered = True).order_by('-id')
        
    
        seven_days_ago = date - timedelta(days=7)
        weakly_order = Order.objects.filter(created_at__gte=seven_days_ago).order_by('-id')
        

        context = {
            'today_count' : today_count,
            'total_count' :total_count,
            'today_total' : today_total,
            'all_total' : all_total,
            'orders':orders,
            'weakly_order': weakly_order,
        }
        
        return render(request, 'admin/adminpanel.html',context)
    else:
        return redirect('login')


@login_required(login_url = 'login')
def productvar(request):
    if request.user.is_superadmin:
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
    else:
        return redirect('login')


@login_required(login_url = 'login')
def productsingle(request,id):
    if request.user.is_superadmin:
        context = {
            'product': Product.objects.get(id=id),
            'multiple' : multiimages.objects.filter(product=id),
        }
        return render(request, 'admin/productsingle.html',context)
    else:
        return redirect('login')


@login_required(login_url = 'login')
def adminaddproduct(request):
    if request.user.is_superadmin:
        categories=Category.objects.all()
        if request.method == 'POST':
            if not request.FILES.get('images'):
                product_name = request.POST['product_name']
                description = request.POST['description']
                price = request.POST['price']
                stock = request.POST['stock']
                imgs = request.FILES['image']
                category_id = request.POST['category']
                category = Category.objects.get(id=category_id)
                
                
                prod = Product.objects.create(
                    product_name=product_name,
                    description=description,
                    price=price,
                    images= imgs,
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
                product_name = request.POST['product_name']
                description = request.POST['description']
                price = request.POST['price']
                stock = request.POST['stock']
                imgs = request.FILES['image']
                category_id = request.POST['category']
                category = Category.objects.get(id=category_id)
                
                
                prod = Product.objects.create(
                    product_name=product_name,
                    description=description,
                    price=price,
                    images= imgs,
                    stock=stock,
                    category=category,
                )
                
                images = request.FILES.getlist('images')
                for image in images:
                    multi = multiimages.objects.create(
                    product = prod,
                    image=image,
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
    else:
        return redirect('login')


@login_required(login_url = 'login')
def adminproducts(request):
    if request.user.is_superadmin:
        Products=Product.objects.all().order_by('id')
        prod_count=Products.count()
        images = multiimages.objects.all()
        context={
            'Products':Products,
            'prod_count':prod_count,
            'images':images,
        }
        return render(request, 'admin/adminproducts.html',context)
    else:
        return redirect('login')
    
    
    
@login_required(login_url = 'login')
def category(request):
    if request.user.is_superadmin:
        Categorys=Category.objects.all().order_by('id')
        Cat_count = Categorys.count()
        context={
            'Categorys':Categorys,
            'Cat_count':Cat_count,
        }
        return render(request, 'admin/category.html',context)
    else:
        return redirect('login')



@login_required(login_url = 'login')
def users(request):
    if request.user.is_superadmin:
        Users=Account.objects.filter(is_admin = False).order_by('id')
        user_count=Users.count()
        context={
            'Users':Users,
            'user_count':user_count,
        }
        return render(request,'admin/users.html',context)
    else:
        return redirect('login')



@login_required(login_url = 'login')
def orders(request):
    if request.user.is_superadmin:
        orders = Order.objects.filter(is_ordered = True).order_by('-id')
        total_count = orders.count()
        context = {
            'orders':orders,
            'total_count' : total_count
        }
        return render(request,'admin/orders.html',context)
    else:
        return redirect('login')


@login_required(login_url = 'login')
def order_details(request,id):
    if request.user.is_superadmin:
        single_order = Order.objects.get(id=id)
        ordered_products = OrderProduct.objects.filter(order_id=single_order.id)
        
        context ={
            'single_order': single_order,
            'products':ordered_products,
        }
        return render(request,'admin/order_details.html',context)
    else:
        return redirect('login')



@login_required(login_url = 'login')
def blockuser(request,id,action):
    if request.user.is_superadmin:
        user=Account.objects.get(id=id)
        if action=='block':
            user.is_active=False
            user.save()
        elif action =='unblock':
            user.is_active=True
            user.save()

        return redirect('users')
    else:
        return redirect('login')


@login_required(login_url = 'login')
def delcategory(request,id):
    if request.user.is_superadmin:
        cat = Category.objects.get(id=id)
        cat.delete()
        return redirect('category')
    else:
        return redirect('login')


@login_required(login_url = 'login')
def change(request,id,action):
    if request.user.is_superadmin:
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
    else:
        return redirect('login')


@login_required(login_url = 'login')
def blockvari(request,id,action):
    if request.user.is_superadmin:
        prod=Variation.object.get(id=id)
        if action=='block':
            prod.is_active=False
            prod.save()
        elif action =='unblock':
            prod.is_active=True
            prod.save()

        return redirect('productvar')
    else:
        return redirect('login')


@login_required(login_url = 'login')
def unlist(request,id,action):
    if request.user.is_superadmin:
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
    else:
        return redirect('login')
        

@login_required(login_url = 'login')       
def multipleimages(request):
    if request.user.is_superadmin:
        if request.method == 'POST':
            product = request.POST['product']
            prod = Product.objects.get(product_name=product)
            
            images = request.FILES.getlist('image')
            for image in images:
                multiimages.objects.create(
                product = prod,
                image=image,
            )
                
            products = multiimages.objects.all().order_by('id')
            paginator = Paginator(products,5)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            products = Product.objects.filter(is_available = True)
            

            context = {
                'variations': paged_products,
                'products': products,
            }
            return render(request, 'admin/multipleimages.html',context)
        else:
            

            products = multiimages.objects.all().order_by('id')
            paginator = Paginator(products,5)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            products = Product.objects.filter(is_available = True)
            

            context = {
                'variations': paged_products,
                'products': products,
            }
            return render(request, 'admin/multipleimages.html',context)
        
    else:
        return redirect('login')


@login_required(login_url = 'login')
def deleteimg(request,id):
    if request.user.is_superadmin:
        prod_data = multiimages.objects.get(id=id)
        prod_data.delete()
        return redirect('multipleimages')
    else:
        return redirect('login')


@login_required(login_url = 'login')
def addcategory(request):
    if request.user.is_superadmin:
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
    else:
        return redirect('login')
    
    
@login_required(login_url = 'login')    
def editcategory(request,id):
    if request.user.is_superadmin:
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
    else:
        return redirect('login')


@login_required(login_url = 'login')    
def editprod(request,id):
    if request.user.is_superadmin:
        if request.method == 'POST':
            single_prod = Product.objects.get(id=id)
            if not request.FILES.get('images'):
                ex1 = Product.objects.filter(id=id).update(
                    product_name = request.POST['product_name'],
                    description = request.POST['description'],
                    price = request.POST['price'],
                    stock = request.POST['stock'],
                )
                return redirect('adminproducts')
            else:
                os.remove(single_prod.images.path)
                single_prod.images = request.FILES['images']
                single_prod.save()
                ex1 = Product.objects.filter(id=id).update(
                    product_name = request.POST['product_name'],
                    description = request.POST['description'],
                    price = request.POST['price'],
                    stock = request.POST['stock'],
                )
                return redirect('adminproducts')
        else:
            prod = Product.objects.get(id=id)
            context = {
                'product':Product.objects.get(id=id),
                'images': multiimages.objects.filter(product = prod)
            }
            return render(request,'admin/editprod.html',context)   
    else:
        return redirect('login')
    

@login_required(login_url = 'login')
def deleteslider(request,id):
    if request.user.is_superadmin:
        slide_data = Slider.objects.get(id=id)
        slide_data.delete()
        return redirect('slideshow')
    else:
        return redirect('login')


        
@login_required(login_url = 'login')        
def slideshow(request):
    if request.user.is_superadmin:
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
    else:
        return redirect('login')
   
    
    
@login_required(login_url = 'login')
def addcoupon(request):
    if request.user.is_superadmin:
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
    else:
        return redirect('login')
        

@login_required(login_url = 'login')
def deletecoupon(request,id):
    if request.user.is_superadmin:
        coupon_data = Coupon.objects.get(id=id)
        coupon_data.delete()
        return redirect('addcoupon') 
    else:
        return redirect('login')  
