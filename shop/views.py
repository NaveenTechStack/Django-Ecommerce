import json
import os
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
import razorpay
from shop.form import CustomUserForm, CustomerProfileForm
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

def home(request):
    products= Products.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})


#favourites Views 
def fav_view_page(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)        
        return render(request,"shop/favourite.html",{"favproducts":fav})
    else:
        return redirect('home')
    
def fav_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            prod_id = data['product_id']
            product_check = Products.objects.get(id=prod_id)
            if product_check:
                if Favourite.objects.filter(user=request.user.id,product_id=prod_id):
                    return JsonResponse({'status':"Product Already in favourites"},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=prod_id)
                    return JsonResponse({'status':"Product Added to favourites"},status=200)
            else:
                return JsonResponse({'status':"No such Product Found"},status=200)
        else:
            return JsonResponse({'status':"Login to Add Favourite"},status=200)
    else:
        return JsonResponse({'status':"Invalid Access"},status=200)

def remove_fav(request,fid):
    if request.user.is_authenticated:
        favitem = Favourite.objects.get(id=fid)       
        favitem.delete()
        return redirect("/favourites")
    else:
        return redirect('home')
    
#Cart Views
def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart:
            value = p.product_qty * p.product.selling_price
            amount = amount + value
        shipping_amount = 40
        totalAmount = amount + shipping_amount
        if amount == 0:
            shipping_amount = 0
            totalAmount = 0        
        return render(request,"shop/cart.html",locals())
    else:
        return redirect('home')
    
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
        c.product_qty += 1
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        cart_product = Cart.objects.filter(user=request.user)
        for p in cart_product:
            tempamount = (p.product.selling_price * p.product_qty)
            amount += tempamount
            
        data = {
            'quantity': c.product_qty,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
        c.product_qty -= 1        
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        cart_product = Cart.objects.filter(user=request.user)
        for p in cart_product:
            tempamount = (p.product.selling_price * p.product_qty)
            amount += tempamount
            
        data = {
            'quantity': c.product_qty,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request,cid):
    if request.user.is_authenticated:
        cartitem = Cart.objects.get(id=cid)       
        cartitem.delete()
        return redirect("/cart")
    else:
        return redirect('home')    


#Product Details View
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            prod_id = data['product_id']
            prod_qty = data['product_qty']
            product_check = Products.objects.get(id=prod_id)
            if product_check:
                if Cart.objects.filter(user=request.user.id,product_id=prod_id):
                    return JsonResponse({'status':"Product Already in Cart"},status=200)
                else:                    
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user,product_id=prod_id,product_qty=prod_qty)
                        return JsonResponse({'status':"Product Added to Cart"},status=200)
                    else:
                        return JsonResponse({'status':"Only "+str(product_check.quantity)+" Quantity Available"},status=200)
            else:
                return JsonResponse({'status':"No such Product Found"},status=200)
        else:
            return JsonResponse({'status':"Login to Continue"},status=200)
    else:
        return JsonResponse({'status':"Invalid Access"},status=200)
    
def product_details(request,cname,pname):
    if(Category.objects.filter(status=1,name=cname)):
        if(Products.objects.filter(name=pname)):
            products= Products.objects.filter(name=pname).first
            return render(request,"shop/products/productDetails.html", {"products":products})
        else:
            messages.warning(request,"No such Product found")
            return redirect('collections')
    else:
        messages.warning(request,"No such Category found")
        return redirect('collections')

#login,logout and register views
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,"Login Success")
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
                return redirect('login_page')
    return render(request,"shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout Success")
    return redirect('/')

def register(request):
    form =CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success you can login Now...!")
            return redirect('login_page')
    return render(request,"shop/register.html",{'form':form})


#collections Views
def collections(request):
    catagory = Category.objects.filter(status=1)
    return render(request,"shop/collections.html", {"catagory":catagory})

def collectionview(request,name):
    if(Category.objects.filter(status=1,name=name)):
        products= Products.objects.filter(category__name=name)
        return render(request,"shop/products/index.html", {"products":products,"category":name})
    else:
        messages.warning(request,"No such Category found")
        return redirect('collections')
    
#profile Views 
class ProfileView(View):
    def get(self,request):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            form = CustomerProfileForm(instance=customer)
            return render(request,"shop/profile/profile.html",locals())
        else:
            return redirect('login_page')
        
    def post(self,request):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            form = CustomerProfileForm(request.POST,instance=customer)
            if form.is_valid():
                user = request.user
                name = form.cleaned_data['name']
                locality = form.cleaned_data['locality']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                zipcode = form.cleaned_data['zipcode']
                mobile = form.cleaned_data['mobile']
                reg = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode,mobile=mobile)
                reg.save()                
                #form.save()
                messages.success(request,"Profile Updated Successfully")               
            else:
                messages.error(request,"Invalid Input Data")
            return render(request,"shop/profile/profile.html",locals())

        else:
            return redirect('login_page')
        
def address(request):
    if request.user.is_authenticated:
        add = Customer.objects.filter(user=request.user)
        return render(request,"shop/profile/address.html",{"add":add})
    else:
        return redirect('login_page')
    
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(id=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,"shop/profile/updateAddress.html",locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(id=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.mobile = form.cleaned_data['mobile']
            add.save()
            messages.success(request,"Address Updated Successfully")
        else:
            messages.error(request,"Invalid Input Data")
        return redirect('address')
    
#checkout Views
class checkout(View):
    def get(self,request):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            add = Customer.objects.filter(user=request.user)
            cart_items = Cart.objects.filter(user=request.user)
            amount = 0
            for p in cart_items:
                value = p.product_qty * p.product.selling_price
                amount = amount + value
            shipping_amount = 40
            totalAmount = amount + shipping_amount
            razoramount = int(totalAmount * 100)
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            data = {
                "amount": razoramount,
                "currency": "INR",
                "receipt": "order_rcptid_11"
            }
            payment_response = client.order.create(data=data)
            orderid = payment_response['id']
            orderStatus = payment_response['status']
            if orderStatus == "created":
                payment = Payment(user=request.user,amount=totalAmount,razorpay_order_id=orderid,razorpay_payment_status=orderStatus)
                payment.save()
            print(payment_response)
            return render(request,"shop/checkout/index.html",locals())
        else:
            return redirect('login_page')
            
def paymentdone(request):   
        order_id = request.GET.get('order_id')
        payment_id = request.GET.get('payment_id')
        custid = request.GET.get('cust_id')
        user = request.user
        customer = Customer.objects.filter(id=custid).first()
        payment = Payment.objects.filter(razorpay_order_id=order_id).first()
        payment.paid = True
        payment.razorpay_payment_id = payment_id
        payment.razorpay_payment_status = "Paid"
        payment.save()
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.product_qty,payment=payment).save()
            c.delete()
        messages.success(request,"Your Order has been Placed Successfully")
        return render(request,"shop/checkout/paymentdone.html");

def orders(request):
    if request.user.is_authenticated:
        order_placed = OrderPlaced.objects.filter(user=request.user)
        return render(request,"shop/orders/orders.html",{"order_placed":order_placed})
    else:
        return redirect('login_page')