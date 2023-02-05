from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Account
from store.models import Product
from category.models import Category
from .models import Slider


def adminpanel(request):
    return render(request, 'admin/adminpanel.html')

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



def blockuser(request,id,action):
    user=Account.objects.get(id=id)
    if action=='block':
        user.is_active=False
        user.save()
    elif action =='unblock':
        user.is_active=True
        user.save()

    return redirect('users')


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
        if not request.FILES.get('cat_image'):
            ex1 = Category.objects.filter(id=id).update(
                category_name = request.POST['category_name'],
                description = request.POST['description'],
            )
            return redirect('category')
        else:
            ex1 = Category.objects.filter(id=id).update(
                category_name = request.POST['category_name'],
                description = request.POST['description'],
                cat_image = request.FILES['cat_image'],
            )
            return redirect('category')
    else:
        context = {
            'category': Category.objects.get(id=id)
        }
        return render(request,'admin/editcategory.html',context)
        
        
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
        
    