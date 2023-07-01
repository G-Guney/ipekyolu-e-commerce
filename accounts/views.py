from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from products.forms import *

# Create your views here.

def sellerRegisterUser(request):
    form = SellerRegisterForm()
    if request.method == 'POST':
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kayıt Başarılı. Giriş Yapabilirsiniz.')
            return redirect('sellerLogin')
    context = {
        'form' : form
    }
    return render(request, 'sellerRegister.html', context)

def sellerLoginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Seller').exists():
                login(request, user)
                messages.success(request, 'Giriş Yapıldı')
                return redirect('sellerPanel')
            else:
                messages.error(request, 'Satıcı değilsiniz. Giriş yapma izniniz yok.')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    return render(request, 'sellerLogin.html')


def customerRegisterUser(request):
    form = CustomerRegisterForm()
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kayıt Başarılı. Giriş Yapabilirsiniz.')
            return redirect('customerLogin')
    context = {
        'form' : form
    }
    return render(request, 'customerRegister.html', context)

def customerLoginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Giriş Yapıldı')
            return redirect('index')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    return render(request, 'customerLogin.html')

def customerLogout(request):
    logout(request)
    messages.warning(request, 'Çıkış Yapıldı.')
    return redirect('index')

@login_required(login_url='customerLogin')
def customerPanel(request):
    user = request.user
    context = {
        'user' : user
    }
    return render(request, 'customerPanel.html',context)

@login_required(login_url='customerLogin')
def myOrders(request):
    payments = Payment.objects.filter(user = request.user, isCompleted = True)
    context = {
        "payments" : payments
    }
    return render (request,'my_orders.html',context)


@login_required(login_url='sellerLogin')
def sellerPanel(request):
    user = request.user
    context = {
        'user' : user
    }
    return render(request, 'sellerPanel.html', context)

@login_required(login_url='sellerLogin')
def addProduct(request):
    # form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Ürün oluşturuldu')
            return redirect('addProduct')
    else:
        form = ProductForm()
    context={'form' : form}
    return render(request, 'addProduct.html', context)

@login_required(login_url='sellerLogin')
def myProducts(request):
    products = Products.objects.filter(seller = request.user)
    if request.method == 'POST':
        productId = request.POST['productId']
        product = Products.objects.get(id=productId)
        product.delete()
        messages.success(request, 'Ürün Kaldırıldı')
        return redirect('myProducts')
    context = {
        'products': products
    }
    return render(request, 'myProducts.html', context)

@login_required(login_url='sellerLogin')
def sellerLogout(request):
    logout(request)
    messages.warning(request, 'Çıkış Yapıldı.')
    return redirect('sellerLogin')