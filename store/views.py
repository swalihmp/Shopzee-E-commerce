from django.shortcuts import render , get_object_or_404,redirect
from .models import Product
from category.models import Category
from cart.models import Cart
from django.db.models import Q

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.



def singleproduct(request,id):
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    context = {
        'item_count':item_count,
        'product': Product.objects.get(id=id),
        'items':items,
    }
    return render(request,'singleproduct.html',context)


def contact(request):
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    context = {
        'item_count':item_count,
        'items':items,
    }
    return render(request,'contact.html',context)

def about(request):
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    context = {
        'item_count':item_count,
        'items':items,
    }
    return render(request,'about.html',context)

def blog(request):
    user = request.user
    user_name = user.username
    products = Product.objects.all()
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    context = {
        'products':products,
        'item_count':item_count,
        'items':items,
    }
    return render(request,'blog.html',context)



def shop(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug !=None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:   
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    context = {
        'item_count':item_count,
        'items':items,
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request,'shop.html',context)


def search_data(request):
    if request.method == 'POST':
        if request.method == "POST":
            searched = request.POST['searched']
            
            
            products1 = Product.objects.filter(Q(product_name__icontains=searched) | Q(description__icontains=searched))
            products2 = Category.objects.filter(Q(category_name__icontains=searched) | Q(description__icontains=searched))
            
            
            
            
            if products1.exists():
                
                products = products1
                product_count = products.count()
        
                user = request.user
                user_name = user.username
                items=Cart.objects.filter(user=user_name)
                item_count = items.count()
            
                context = {
                    'item_count':item_count,
                    'items':items,
                    'products':products,
                    'product_count': product_count,
                }
                return render(request,'shop.html',context)
            elif products2.exists():
                
                products = products2
                product_count = products.count()
        
                user = request.user
                user_name = user.username
                items=Cart.objects.filter(user=user_name)
                item_count = items.count()
            
                context = {
                    'item_count':item_count,
                    'items':items,
                    'products':products,
                    'product_count': product_count,
                }
                return render(request,'shop.html',context)
        return redirect('store')
    return redirect('store')