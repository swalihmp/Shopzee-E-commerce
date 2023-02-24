from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart,Wishlist
from store.models import Product
from .models import Order,Payment,OrderProduct
from datetime import datetime
import datetime
import json
from accounts.models import Address,UserProfile,Account
from adminp.models import Coupon


from django.core.mail import EmailMessage
from django.template.loader import render_to_string



# Create your views here.
def payment(request):
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user=request.user, is_ordered=False , order_number=body['orderID'])
    
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    
    user = request.user
    user_name = user.username
    cart_items = Cart.objects.filter(user=user_name)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id 
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.color = item.color
        orderproduct.size = item.size
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        
        orderproduct.save()
        
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        
    coupons = order.coupon
    print(coupons)
    
    try:
        getcoupon = Coupon.objects.get(coupon_id=coupons)
    except Coupon.DoesNotExist:
        getcoupon = None
    else :
        quantity = 1
        getcoupon.allowed_users -= quantity
        getcoupon.save()
    
    Cart.objects.filter(user=user_name).delete()
    
    
    mail_subject = "Thank You For You Order"
    message = render_to_string('orders/order_recieve_email.html',{
        'user': request.user,
        'order': order,
    })
    
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message, to=[to_email])
    send_email.send()
    
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
        
    return JsonResponse(data)


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        
        products = Product.objects.all().filter(is_available=True)
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
        
        
        order = Order.objects.get(order_number=order_number, is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price*i.quantity
        payment = Payment.objects.get(payment_id=transID)
        
        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID': payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
            'item_count':item_count,
            'products':products,
            'items':items,
            'total':total,
            'witem_count':witem_count,
            'witems':witems,
        }
        return render(request, 'orders/order_complete.html',context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('HomePage')
    
    
    
    
def place_order(request):
    user = request.user
    user_name = user.username
    
    cart_items = Cart.objects.filter(user=user_name)
    cart_count = cart_items.count()
    
    
    total =0
    is_available = True
    total_quantity = 0
    for i in range(len(cart_items)):
        x = cart_items[i].product.price*cart_items[i].quantity
        total_quantity = total_quantity + cart_items[i].quantity
        total = total+x
        
        if cart_items[i].product.stock < cart_items[i].quantity :
            is_available = False
            prod = cart_items[i].product.product_name
        else: 
            is_available = True
    if (is_available == False):
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
            'prod':prod
        }
        messages.error(request,'Gone Zero Stock....!')
        return render(request,'checkout.html',context)
    else :
        tax = 0
        tax = (2*total)/100
        grand_total = total + tax
        
        if cart_count <= 0:
            return redirect('store')
        
        
        elif request.method == 'POST':
            total = request.POST['gtotal']
            print(total)
            tax = 0
            tax = (2*int(total))/100
            grand_total = int(total) + tax
            
            choice = request.POST['payment']
            data = Order()
            data.user = user
            data.first_name = request.POST['first_name']
            data.phone = request.POST['phone']
            data.address_line_1 = request.POST['address_line_1']
            data.address_line_2 = request.POST['address_line_2']
            data.post_code = request.POST['post_code']
            data.city = request.POST['city']
            data.country = request.POST['country']
            data.state = request.POST['state']
            data.order_total = grand_total
            data.tax = tax
            data.created_at = datetime.datetime.now()
            if request.POST['coupon']:
                try:
                    coupons = Coupon.objects.get(coupon_id=request.POST['coupon'])
                except Coupon.DoesNotExist:
                    data.coupon = "None"
                else :
                    date = datetime.datetime.now().date()
                    sdate = coupons.activ_date
                    edate = coupons.exp_date
                    minimum = coupons.min_amount
                    users = coupons.allowed_users
                    if ( int(minimum)<int(total) and sdate <= date <= edate and users>0):
                        data.coupon = request.POST['coupon']
                
            data.save()
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            
            order_number = current_date + str(data.id)
            
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=user, is_ordered=False, order_number = order_number)
            context ={
                'order': order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
            }
            if 'checked' in request.POST :
                user = request.user
                profile=UserProfile.objects.get(user=user)
                exist = Address.objects.filter(profile=profile,address_line_1=request.POST['address_line_1'],address_line_2=request.POST['address_line_2'],name=request.POST['first_name'],phone=request.POST['phone'],city=request.POST['city'],state=request.POST['state'],country=request.POST['country'],zip_code=request.POST['post_code'])
                if not exist.exists():
                    Address.objects.create(
                        profile = profile,
                        address_line_1 = request.POST['address_line_1'],
                        address_line_2 = request.POST['address_line_2'],
                        name = request.POST['first_name'],
                        phone = request.POST['phone'],
                        city = request.POST['city'],
                        state = request.POST['state'],
                        country = request.POST['country'],
                        zip_code = request.POST['post_code'],
                    )
                
            if choice == "COD":
                
                order = Order.objects.get(user=request.user, is_ordered=False , order_number=order_number)
            
                payment = Payment(
                    user = request.user,
                    payment_id = "COD",
                    payment_method = "COD",
                    amount_paid = order.order_total,
                    status = "COMPLETED",
                )
                payment.save()
                order.payment = payment
                order.is_ordered = True
                order.save()
                
                
                user = request.user
                user_name = user.username
                cart_items = Cart.objects.filter(user=user_name)
                
                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id 
                    orderproduct.payment = payment
                    orderproduct.user_id = request.user.id
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.color = item.color
                    orderproduct.size = item.size
                    orderproduct.product_price = item.product.price
                    orderproduct.ordered = True
                    
                    orderproduct.save()
                    
                    product = Product.objects.get(id=item.product_id)
                    product.stock -= item.quantity
                    product.save()
                    
                coupons = order.coupon
                
                
                try:
                    getcoupon = Coupon.objects.get(coupon_id=coupons)
                except Coupon.DoesNotExist:
                    getcoupon = None
                else :
                    quantity = 1
                    getcoupon.allowed_users -= quantity
                    getcoupon.save()
                
                        
                Cart.objects.filter(user=user_name).delete()
                
                
                mail_subject = "Thank You For You Order"
                message = render_to_string('orders/order_recieve_email.html',{
                    'user': request.user,
                    'order': order,
                })
                
                to_email = request.user.email
                send_email = EmailMessage(mail_subject,message, to=[to_email])
                send_email.send()
            
                return render(request, 'orders/cod_order_complete.html')
                    
            else:
                return render(request, 'orders/payments.html',context)
        else:
            return redirect('checkout')
    

def cod_order_complete(requset):
    return render(requset, 'orders/cod_order_complete.html')
