from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def home(request):
    products=product.objects.filter(trending=1)
    return render(request,'shop/index.html',{'products':products})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Hey "+str(request.user)+"! Logged in Successfully")
                return redirect('home')
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect('login')
        return render(request,'shop/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect('home')

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You Can Login Now!")
            return redirect('login')
    return render(request,'shop/register.html',{'form':form})

def collections(request):
    Category=category.objects.filter(status=0)
    return render(request,'shop/collections.html',{"category":Category})

def collectionsview(request,cname):
    if(category.objects.filter(status=0,name=cname)):
        products=product.objects.filter(category__name=cname)
        return render(request,'shop/products/index.html',{"products":products,'category_name':cname})
    else:
        messages.warning(request,"No Such Category Found")
        return redirect('collections')
    
def product_details(request,cname,pname):
    if(category.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            products=product.objects.get(name=pname,status=0) #filter.first()
            return render(request,'shop/products/product_details.html',{'products':products})
        else:
            messages.warning(request,"No Such Product Found")
            return redirect('collections')
    else:
        messages.warning(request,"No Such Category Found")
        return redirect('collections')
    
def add_to_cart(request):
    pass