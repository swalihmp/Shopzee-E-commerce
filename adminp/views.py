from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Account


def adminpanel(request):
    return render(request, 'admin/adminpanel.html')

def users(request):
    Users=Account.objects.filter(is_admin = False)
    user_count=Users.count()
    context={
        'Users':Users,
        'user_count':user_count,
    }
    return render(request,'admin/users.html',context)

def deleteuser(request,id):
    user=Account.objects.get(id=id)
    user.delete()
    Users=Account.objects.filter(is_admin = False)
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
    Users=Account.objects.filter(is_admin = False)
    user_count=Users.count()
    context={
        'Users':Users,
        'user_count':user_count,
    }
    return render(request,'admin/users.html',context)