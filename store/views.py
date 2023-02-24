from django.shortcuts import render , get_object_or_404,redirect
from .models import Product, multiimages ,Review_Rating
from category.models import Category
from cart.models import Cart , Wishlist
from django.db.models import Q
from orders.models import Order,OrderProduct
from accounts.models import UserProfile

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.




def singleproduct(request,id):
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    total =0
    for i in range(len(items)):
        x = items[i].product.price*items[i].quantity
        total = total+x
    
    witems=Wishlist.objects.filter(user=user_name)
    witem_count = witems.count()
    
    multiple = multiimages.objects.filter(product=id)
    similar = Product.objects.filter()

    
    single_product = Product.objects.get(id=id)
    cat = single_product.category
    
    try :
        if request.user.is_authenticated:
            orderproduct = OrderProduct.objects.filter(user=request.user,product=single_product).exists()
            order_product = OrderProduct.objects.filter(user=request.user,product=single_product).first()
        else:
            orderproduct = None
            order_product = None
    except OrderProduct.DoesNotExist:
        orderproduct = None
        order_product = None
    
    
    reviews = Review_Rating.objects.filter(product_id=single_product.id,status=True)
    similar = Product.objects.filter(category=cat).exclude(product_name=single_product.product_name)
    
    context = {
        'item_count':item_count,
        'product': Product.objects.get(id=id),
        'items':items,
        'witem_count':witem_count,
        'witems':witems,
        'total':total,
        'multiple':multiple,
        'similar' : similar,
        'orderproduct':orderproduct,
        'order_product':order_product,
        'reviews':reviews,
    }
    return render(request,'singleproduct.html',context)


def contact(request):
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    total =0
    for i in range(len(items)):
        x = items[i].product.price*items[i].quantity
        total = total+x
    
    witems=Wishlist.objects.filter(user=user_name)
    witem_count = witems.count()
    
    context = {
        'item_count':item_count,
        'items':items,
        'witem_count':witem_count,
        'witems':witems,
        'total':total,
    }
    return render(request,'contact.html',context)

def about(request):
    user = request.user
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    total =0
    for i in range(len(items)):
        x = items[i].product.price*items[i].quantity
        total = total+x
    
    witems=Wishlist.objects.filter(user=user_name)
    witem_count = witems.count()
    
    context = {
        'item_count':item_count,
        'items':items,
        'witem_count':witem_count,
        'witems':witems,
        'total':total,
    }
    return render(request,'about.html',context)

def blog(request):
    user = request.user
    user_name = user.username
    products = Product.objects.all()
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    total =0
    for i in range(len(items)):
        x = items[i].product.price*items[i].quantity
        total = total+x
    
    witems=Wishlist.objects.filter(user=user_name)
    witem_count = witems.count()
    
    context = {
        'products':products,
        'item_count':item_count,
        'items':items,
        'witem_count':witem_count,
        'witems':witems,
        'total':total,
        
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
    
    total =0
    for i in range(len(items)):
        x = items[i].product.price*items[i].quantity
        total = total+x
    
    witems=Wishlist.objects.filter(user=user_name)
    witem_count = witems.count()
    
    context = {
        'item_count':item_count,
        'items':items,
        'products': paged_products,
        'product_count': product_count,
        'witem_count':witem_count,
        'witems':witems,
        'total':total,
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
                
                total =0
                for i in range(len(items)):
                    x = items[i].product.price*items[i].quantity
                    total = total+x
                
                witems=Wishlist.objects.filter(user=user_name)
                witem_count = witems.count()
            
                context = {
                    'item_count':item_count,
                    'items':items,
                    'products':products,
                    'product_count': product_count,
                    'witem_count':witem_count,
                    'witems':witems,
                    'total':total,
                }
                return render(request,'shop.html',context)
            elif products2.exists():
                
                products = products2
                product_count = products.count()
        
                user = request.user
                user_name = user.username
                items=Cart.objects.filter(user=user_name)
                item_count = items.count()
                
                total =0
                for i in range(len(items)):
                    x = items[i].product.price*items[i].quantity
                    total = total+x
                
                witems=Wishlist.objects.filter(user=user_name)
                witem_count = witems.count()
            
                context = {
                    'item_count':item_count,
                    'items':items,
                    'products':products,
                    'product_count': product_count,
                    'witem_count':witem_count,
                    'witems':witems,
                    'total':total,
                }
                return render(request,'shop.html',context)
        return redirect('store')
    return redirect('store')

def submit_review(request,id):
    product = Product.objects.get(id=id)
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = Review_Rating.objects.get(user=request.user,product=product)
            subject = request.POST['subject']
            reviews = request.POST['reviews']
            rating = request.POST['rating']
            
            Review_Rating.objects.filter(user=request.user,product=product).update(
                subject = subject,
                reviews = reviews,
                rating = rating,
            )
            return redirect(url)
        except Review_Rating.DoesNotExist:
            user= request.user
            product = Product.objects.get(id=id)
            subject = request.POST['subject']
            reviews = request.POST['reviews']
            rating = request.POST['rating']
            
            Review_Rating.objects.create(
                user = user,
                product = product,
                subject = subject,
                reviews = reviews,
                rating = rating,
            )
            return redirect(url)
    return redirect(url)


            