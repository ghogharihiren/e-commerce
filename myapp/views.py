from django.shortcuts import render,redirect
from .forms import*
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password

def index(request):
    pro=Product.objects.all()
    user=User.objects.all()[::-1]
    if request.user.is_authenticated:
        pro1=Buyproduct.objects.all()
        if request.user.role == 'seller':
            if request.user.verification == True:
                return render(request,'seller/seller-index.html',{'pro':pro1})
            else:
                messages.info(request,'Your account not verifay')
                logout(request)
                return redirect('login')
        elif request.user.role == 'buyer':
            return render(request,'index.html',{'pro':pro})
        else:
            return render(request,'admin/admin-index.html',{'user':user})
    else:
        return render(request,'index.html',{'pro':pro})
            

def user_login(request):
    if request.user.is_authenticated:
            return redirect('index')
    else:
        form1=Userlogin()
        if request.method == "POST":
            form=Userlogin(request=request,data=request.POST)
            if form.is_valid():
                user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
                if user is not None:
                    login(request,user)
                    return redirect('index')     
                else:
                    messages.info(request,'Enter correct username or password')
                    return render(request,'login.html',{'form':form1})
            else:
                print(form.errors)
                messages.info(request,'Enter correct username or password')
                return render(request,'login.html',{'form':form1})    
        return render(request,'login.html',{'form':form1}) 


def register(request):
    form=RegisterForm()
    if request.method == "POST":
        form1=RegisterForm(request.POST)
        if form1.is_valid():
            form1.save()
            messages.success(request,'your account crated')
            return redirect('login')
        else:
            messages.info(request,'Enter the valid data!')
            return render(request,'register.html',{'form':form})     
    return render(request,'register.html',{'form':form})

def forgot_password(request):    
    if request.method =="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            password = ''.join(random.choices('qwyertovghlk34579385',k=9))
            subject="Rest Password"
            message = f"""Hello {user.username},Your New password is {password}"""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'],]
            send_mail( subject, message, email_from, recipient_list )
            user.password=make_password(password)
            user.save()
            messages.success(request,'New password send in your email')
            return redirect('login')
        except:
            messages.info(request,'Enter the valid email addres')
            return render(request,'forgot-password.html')         
    return render(request,'forgot-password.html')  


@login_required(login_url='/login/')
def change_password(request):
    p=PasswordChangeForm(user=request.user)
    if request.method=="POST":
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            update_session_auth_hash(request,form.user)
            form.save()
            messages.success(request,'your password update')
            return redirect('login')
        else:
            messages.info(request,'enter the correct password')
            return render(request,'change-password.html',{'form':p})   
    return render(request,'change-password.html',{'form':p}) 

@login_required(login_url='/login/')
def edit_profile(request):
    form=EditprofileForm(instance=request.user)
    if request.method == "POST":
        form1=EditprofileForm(request.POST,instance=request.user)
        if form1.is_valid():
            form1.save()
            messages.success(request,'Your profile Update')
            return redirect('profile')
        else:
            messages.info(request,'Enter the valid data')
            return render(request,'profile.html',{'form':form})
    return render(request,'profile.html',{'form':form})
        


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('login')

#-------------------------------------------------------Admin-----------------------------------
@login_required(login_url='/login/')
def admin_index(request):
    user=User.objects.all()
    return render(request,'admin/admin-index.html',{'user':user})


@login_required(login_url='/login/')
def seller_list(request):
    user=User.objects.filter(role='seller')[::-1]
    return render(request,'admin/seller-list.html',{'user':user})


@login_required(login_url='/login/')
def buyer_list(request):
    user=User.objects.filter(role='buyer')[::-1]
    return render(request,'admin/buyer-list.html',{'user':user})

@login_required(login_url='/login/')
def verification(request,pk):
    user=User.objects.get(id=pk)
    user.verification = True
    user.save()
    if user.role =='seller':
       return redirect('seller-list')
    else:
        return redirect('buyer-list')
#----------------------------------------------seller-----------------------------------------

@login_required(login_url='/login/')
def my_product(request):
    pro=Product.objects.filter(seller=request.user)
    return render(request,'seller/my-product.html',{'pro':pro})

@login_required(login_url='/login/')
def seller_index(request):
    pro=Buyproduct.objects.all()
    return render(request,'seller/seller-index.html',{'pro':pro})

@login_required(login_url='/login/')
def add_product(request):
    form=AddproductForm()
    if request.method == "POST":
        form1=AddproductForm(request.POST,request.FILES)
        if form1.is_valid():
            h=form1.save(commit=False)
            h.seller=request.user
            h.save()
            messages.success(request,'your product add successfully')
            return redirect('seller-index')
        else:
            messages.info(request,'Enter the correct detail')
            return render(request,'seller/add-product.html',{'form':form})  
    return render(request,'seller/add-product.html',{'form':form})


@login_required(login_url='/login/')
def delete_product(request,pk):
    pro=Product.objects.get(id=pk)
    pro.delete()
    return redirect('seller-index')

@login_required(login_url='/login/')
def edit_product(request,pk):
    pro=Product.objects.get(id=pk)
    form=EditproductForm(instance=pro)
    if request.method == "POST":
        form1=EditproductForm(request.POST,request.FILES,instance=pro)
        if form1.is_valid():
            form1.save()
            messages.success(request,'your product update successfully')
            return redirect('seller-index')
        else:
            messages.info(request,'Enter the valid details')
            return render(request,'seller/edit-product.html',{'form':form,'pro':pro})      
    return render(request,'seller/edit-product.html',{'form':form,'pro':pro})

@login_required(login_url='/login/')
def view_ordered(request,pk):
    pro=Buyproduct.objects.get(id=pk)
    return render(request,'seller/view-ordered.html',{'pro':pro})

@login_required(login_url='/login/')
def packing(request,pk):
    pro=Buyproduct.objects.get(id=pk)
    pro.status = 'packing'
    pro.save()
    return redirect('seller-index')

@login_required(login_url='/login/')
def ready_to_dispatch(request,pk):
    pro=Buyproduct.objects.get(id=pk)
    pro.status = 'ready to dispatch'
    pro.save()
    return redirect('seller-index')


@login_required(login_url='/login/')
def on_the_way(request,pk):
    pro=Buyproduct.objects.get(id=pk)
    pro.status = 'on the way'
    pro.save()
    return redirect('seller-index')


@login_required(login_url='/login/')
def odered_complate(request,pk):
    pro=Buyproduct.objects.get(id=pk)
    pro.status = 'odered complate'
    pro.save()
    return redirect('seller-index')
#--------------------------------------buyer-----------------------------------------------------------

def view_product(request,pk):
    pro=Product.objects.get(id=pk)
    return render(request,'view-product.html',{'pro':pro})

def category_list(request,id):
    if id == '1':
        pro=Product.objects.filter(category='electronic')
        return render(request,'category-list.html',{'pro':pro})
    elif id =='2':
        pro=Product.objects.filter(category='fashion')
        return render(request,'category-list.html',{'pro':pro})
    elif id =='3':
        pro=Product.objects.filter(category='home and kitchen')
        return render(request,'category-list.html',{'pro':pro})
    elif id =='4':
        pro=Product.objects.filter(category='travel')
        return render(request,'category-list.html',{'pro':pro})
    elif id =='5':
        pro=Product.objects.filter(category='toy')
        return render(request,'category-list.html',{'pro':pro})
    elif id =='6':
        pro=Product.objects.filter(category='beauty')
        return render(request,'category-list.html',{'pro':pro})
    elif id =='7':
        pro=Product.objects.filter(category='food')
        return render(request,'category-list.html',{'pro':pro})
    else:
        pro=Product.objects.filter(category='stationery')
        return render(request,'category-list.html',{'pro':pro})
        
@login_required(login_url='/login/')
def add_to_cart(request,pk):
    pro=Product.objects.get(id=pk)
    my=Mycart.objects.filter(user=request.user)
    if pro not in my:
        if request.method =="POST":
            form=AddcartForm(request.POST)
            q=request.POST['quantity']
            if pro.quantity >= int(q): 
                if form.is_valid():
                    f=form.save(commit=False)
                    f.user=request.user
                    f.product=pro
                    f.save()
                    messages.success(request,'product added cart')
                    return redirect('my-cart')
                else:
                    messages.info(request,'enter the valid data')
                    return render(request,'view-product.html',{'pro':pro})
            else:
                messages.info(request,'your quantity in more then available quantity')  
                return render(request,'view-product.html',{'pro':pro})
        return render(request,'view-product.html',{'pro':pro})
    else:
        messages.info(request,'product alreday in cart')
        return render(request,'view-product.html',{'pro':pro})    
                
@login_required(login_url='/login/')                
def my_cart(request):
    cart=Mycart.objects.filter(user=request.user)[::-1]
    amount=0.0
    for c in cart:
        total=(c.quantity*c.product.price)
        amount +=total   
    return render(request,'buyer/my-cart.html',{'cart':cart,'amount':amount})    

@login_required(login_url='/login/')
def remove_to_cart(request,pk):
    cart=Mycart.objects.get(id=pk)
    cart.delete()
    return redirect('my-cart') 

@login_required(login_url='/login/')
def edit_to_cart(request,pk):
    cart=Mycart.objects.get(id=pk)
    form1=EditcartForm(instance=cart)
    if request.method =="POST":
        form=EditcartForm(request.POST,instance=cart)
        v=request.POST['quantity']
        if cart.product.quantity >= int(v):
            if form.is_valid():
                form.save()
                messages.success(request,'update your cart')
                return redirect('my-cart')
            else:
                messages.info(request,'Enter the valid data')
                return render(request,'buyer/edit-to-cart.html',{'form':form1,'pro':cart})    
        else:
            messages.info(request,'your quantity in more then available quantity')  
            return render(request,'buyer/edit-to-cart.html',{'form':form1,'pro':cart})             
    return render(request,'buyer/edit-to-cart.html',{'form':form1,'pro':cart})    

@login_required(login_url='/login/')
def checkout(request):
    cart=Mycart.objects.filter(user=request.user)
    form=BuyproductForm()
    t=0.0
    for c in cart:
        my=c.total_cost
        t +=my
    if request.method =="POST":
        for c in cart:
            form1=BuyproductForm(request.POST)
            if form1.is_valid():
                a=form1.save(commit=False)
                a.product=c.product
                a.total_amount=c.total_cost
                a.quantity=c.quantity
                a.user=request.user
                a.save()
                c.product.quantity -= c.quantity
                c.product.save()
                c.delete()
            else: 
                messages.info(request,'enter the valid data')
                return render(request,'buyer/checkout.html',{'cart':cart,'form':form,'t':t})     
        messages.success(request,'product buy successfully ')
        return redirect('my-buy')     
    else:
        return render(request,'buyer/checkout.html',{'cart':cart,'form':form,'t':t})


@login_required(login_url='/login/')
def buy_now(request,pk):
    pro=Product.objects.get(id=pk)
    form=BuyproductForm()
    if request.method =="POST":
        form1=BuyproductForm(request.POST)
        v=request.POST['quantity']
        if pro.quantity >= int(v):
            if form1.is_valid():
                c=form1.save(commit=False)
                c.total_amount=pro.price *int(v)
                c.product=pro
                c.user=request.user
                c.quantity=v
                c.save()
                pro.quantity -= int(v)
                pro.save()
                messages.success(request,'product buy successfully ')
                return redirect('my-buy')
            else:
                messages.info(request,'enter the valid data')
                return render(request,'buyer/buy-now.html',{'form':form,'pro':pro})
        else:
            messages.info(request,'your quantity in more then available quantity')  
            return render(request,'buyer/buy-now.html',{'form':form,'pro':pro})          
    return render(request,'buyer/buy-now.html',{'form':form,'pro':pro})

@login_required(login_url='/login/')
def my_buy(request):
    buy=Buyproduct.objects.filter(user=request.user)[::-1]
    return render(request,'buyer/my-buy.html',{'buy':buy})

def search_product(request):
    if request.method == "GET":
        search=request.GET.get('search')
        if search:
            pro=Product.objects.filter(product_name__icontains=search)
            pro1=Product.objects.filter(category__icontains=search)
            return render(request,'search.html',{'pro':pro,'pro':pro1})
        
def cancel_ordered(request,pk):
    pro=Buyproduct.objects.get(id=pk)
    pro.product.quantity += pro.quantity
    pro.product.save()
    pro.delete() 
    return redirect('my-buy')   

def edit_ordered(request,pk):
    pro=Buyproduct.objects.get(id=pk)
    if pro.status == 'pending'  or pro.status == 'packing':
        form=EditduyproductForm(instance=pro)
        if request.method=="POST":
            pro.product.quantity += pro.quantity
            pro.product.save()
            form1=EditduyproductForm(request.POST,instance=pro)
            a=request.POST['quantity']
            amount=pro.product.price * int(a)
            if form1.is_valid():
                v=form1.save(commit=False)
                v.total_amount=amount
                v.product.quantity -= int(a)
                v.product.save()
                v.save()
                messages.success(request,'Your ordered update')
                return redirect('my-buy')
        else:
            return render(request,'buyer/edit-ordered.html',{'form':form,'pro':pro})    
    else:
        messages.info(request,'sorry your ordered dispatch')
        return redirect('my-buy')