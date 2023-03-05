from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account, UserProfile ,Address
from store.models import Product
from cart.models import Cart,Wishlist
from orders.models import Order,OrderProduct
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name = first_name , last_name = last_name, email=email, username=username,password=password)
            user.phone_number = phone_number
            user.save()
            
            
            current_site = get_current_site(request)
            mail_subject = "Pls Activate your Account"
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain': current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject,message, to=[to_email])
            send_email.send()
            
            messages.success(request,'Regetration successful,check email for vertification')
            return redirect("register")
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()

        messages.success(request, 'Your account is activated..!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')



def login(request):
    if request.user.is_authenticated:
        return redirect('HomePage')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            
            user=auth.authenticate(email=email, password=password)
            
            if user is not None:
                if user.is_admin:
                    auth.login(request,user)
                    return redirect('adminpanel')
                else:
                    auth.login(request,user)
                    if 'cart' in request.session:
                        session_cart = request.session['cart']
                        for id, product_data in session_cart.items():
                            color = product_data['color']
                            size = product_data['size']
                            product = Product.objects.get(id=id)
                            user = request.user
                            uid = user.username
                            
                            if Cart.objects.filter(product=product,user=uid,color=color,size=size).exists():
                                auth.login(request,user)
                                return redirect('HomePage')
                            else:
                                Cart.objects.create(product=product,user=uid,color=color,size=size)
                                auth.login(request,user)
                                return redirect('HomePage')
                    else:
                        auth.login(request,user)
                        return redirect('HomePage')
            else:
                messages.error(request, "Invalid Credentials....")
                return redirect('login')
        return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    request.session.flush()
    auth.logout(request)
    return redirect('HomePage')



@login_required(login_url = 'login')
def dashboard(request):
    user = request.user
    profile=UserProfile.objects.get(user=user)
    addresses = Address.objects.filter(profile=profile)
    
    user_name = user.username
    items=Cart.objects.filter(user=user_name)
    item_count = items.count()
    
    witems=Wishlist.objects.filter(user=user_name)
    witem_count = witems.count()
    
    
    total =0
    for i in range(len(items)):
        x = items[i].product.price*items[i].quantity
        total = total+x
        
    orders = Order.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(orders,3)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    
    context={
        'profile':profile,
        'addresses':addresses,
        'item_count':item_count,
        'items':items,
        'total':total,
        'witem_count':witem_count,
        'witems':witems,
        'orders' : paged_orders,
    }
    
    return render(request, 'accounts/dashboard.html',context)


@login_required(login_url = 'login')
def editprofile(request):
    if request.user.is_authenticated:
        user = request.user
        single_user = UserProfile.objects.get(user=user)
        if request.method == 'POST':
            if not request.FILES.get('profile_picture'):
                ex1 = Account.objects.filter(email=request.user.email).update(
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    username = request.POST['username'],
                    phone_number = request.POST['phone_number'],
                )
                return redirect('dashboard')
            else:
                single_user.profile_picture = request.FILES['profile_picture']
                single_user.save()
                ex1 = Account.objects.filter(email=request.user.email).update(
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    username = request.POST['username'],
                    phone_number = request.POST['phone_number'],
                )
                return redirect('dashboard')
        else :
            user = request.user
            profile=UserProfile.objects.get(user=user)
            addresses = Address.objects.filter(profile=profile)
            
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
                'profile':profile,
                'addresses':addresses,
                'item_count':item_count,
                'items':items,
                'total':total,
                'witem_count':witem_count,
                'witems':witems,
            }
            
            return render(request, 'accounts/editprofile.html',context)
    else:
        return redirect('login')



@login_required(login_url = 'login')
def add_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            profile=UserProfile.objects.get(user=user)
            Address.objects.create(
                profile = profile,
                address_line_1 = request.POST['address_line_1'],
                address_line_2 = request.POST['address_line_2'],
                name = request.POST['first_name'],
                phone = request.POST['phone'],
                city = request.POST['city'],
                state = request.POST['state'],
                country = request.POST['country'],
                zip_code = request.POST['zip_code'],
            )
            return redirect('dashboard')
        else :
            user = request.user
            profile=UserProfile.objects.get(user=user)
            addresses = Address.objects.filter(profile=profile)
            
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
                'profile':profile,
                'addresses':addresses,
                'item_count':item_count,
                'items':items,
                'total':total,
                'witem_count':witem_count,
                'witems':witems,
            }
            return render(request, 'accounts/add_address.html',context)
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
           user = Account.objects.get(email__exact=email)
           
           current_site = get_current_site(request)
           mail_subject = "Pls Reset Your Password"
           message = render_to_string('accounts/reset_password_email.html',{
            'user':user,
            'domain': current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
           })
            
           to_email = email
           send_email = EmailMessage(mail_subject,message, to=[to_email])
           send_email.send() 
           messages.success(request, 'Password reset link has been send to your email')
           return redirect('login')
        
        else:
            messages.error(request,'Acccount Does Not Exists....!')
            return redirect('forgot_password')
    else:
        return render(request, 'accounts/forgot_password.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Pls Reset your Password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been Expired')
        return redirect('login')
    
def resetpassword(request):
    if request.method == 'POST':
        password=request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Completed')
            return redirect('login')
        
        else:
            messages.error(request, 'Password Does Not Match')
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetpassword.html')
    
def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            oldpass=request.POST['oldpass']
            password=request.POST['password']
            password1=request.POST['password1']
            
            user = Account.objects.get(username__exact=request.user.username)

            success = user.check_password(oldpass)
            if success:
                if password == password1:
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password Change Completed')
                    auth.logout(request)
                    return redirect('login')
                    
                else:
                    messages.success(request,'Passwords Must Be Same...')
                    return render(request,'accounts/changepassword.html')
            else:
                messages.error(request, "Invalid Old Password....")
                return render(request,'accounts/changepassword.html')
        else:
            return render(request,'accounts/changepassword.html')
    else:
        return redirect('login')


def invoice(request,id):
    single_order = Order.objects.get(id=id)
    ordered_products = OrderProduct.objects.filter(order_id=single_order.id)
    
    context ={
        'single_order': single_order,
        'products':ordered_products,
    }
    return render(request,'accounts/invoice.html',context)