from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
import iyzipay
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
import pprint
from django.core.cache import cache

# Create your views here.


#-----------Payment-------------------
api_key = 'sandbox-MMZA5X20scbfA7sALHaqd2ruJ6xMd0BA'
secret_key = 'sandbox-LKuOgisfAwUYuiCwxtM4ebe8lde1JCDi'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}
sozlukToken = list()

def payment(request):
    context = dict()
    user = request.user
    payment_obj = Payment.objects.get(user = user, isCompleted = False)
    buyer={
        'id': 'BY789',
        'name': user.username,
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address={
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]

    request={
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': payment_obj.total,
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:8000/products/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(type(json_content))
    print(json_content["checkoutFormContent"])
    print("************************")
    print(json_content["token"])
    token = json_content["token"]
    cache.set('token', token)
    print("************************")
    sozlukToken.append(json_content["token"])
    return HttpResponse(f'<div id="iyzipay-checkout-form" class="responsive">{json_content["checkoutFormContent"]}</div>')


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('index')
    token = cache.get('token')
    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': token
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda 
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    print(sozlukToken)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return redirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return redirect(reverse('failure'), context)

    return HttpResponse(url)

def success(request):
    payment = Payment.objects.get(user = request.user, isCompleted = False)
    payment.isCompleted = True
    payment.save()
    cart = ShoppingCart.objects.filter(user = request.user, isPaid = False)
    for i in cart:
        i.isPaid = True
        i.save()
    messages.success(request, 'Ödeme Başarılı...')
    return redirect('customerPanel')


def fail(request):
    messages.error(request, 'Ödeme Başarısız!')
    return redirect('cart')

#-----------


def products(request):
    products = Products.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            productId = request.POST['productId']
            unit = request.POST['unit']
            cartProduct = Products.objects.get(id = productId)
            if ShoppingCart.objects.filter(user = request.user, product = cartProduct, isPaid = False).exists():
                cart = ShoppingCart.objects.get(user = request.user, product = cartProduct, isPaid = False)
                cart.unit += int(unit)
                cart.save()
            else:
                cart = ShoppingCart.objects.create(
                    user = request.user,
                    product = cartProduct,
                    unit = unit,
                    total = cartProduct.price * int(unit),
                    isPaid = False
                )
                cart.save()
            return redirect('products-list')
        else:
            messages.warning(request, 'Lütfen Giriş Yapınız')
            return redirect('customerLogin')
    context = {
        'products' : products,
    }
    return render(request, 'products.html', context)

def categories(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'categories.html', context)

def products_by_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products = Products.objects.filter(category=category)
    if request.method == 'POST':
        if request.user.is_authenticated:
            productId = request.POST['productId']
            unit = request.POST['unit']
            cartProduct = Products.objects.get(id = productId)
            if ShoppingCart.objects.filter(user = request.user, product = cartProduct, isPaid = False).exists():
                cart = ShoppingCart.objects.get(user = request.user, product = cartProduct, isPaid = False)
                cart.unit += int(unit)
                cart.save()
            else:
                cart = ShoppingCart.objects.create(
                    user = request.user,
                    product = cartProduct,
                    unit = unit,
                    total = cartProduct.price * int(unit),
                    isPaid = False
                )
                cart.save()
            return redirect('products_by_category', category_slug=category_slug) 
        else:
            messages.warning(request, 'Lütfen Giriş Yapınız')
            return redirect('customerLogin')
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products.html', context)

def product_detail(request, product_id, category_slug):
    product = get_object_or_404(Products, id=product_id, category__slug=category_slug)
    category = Category.objects.get(slug=category_slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            productId = request.POST['productId']
            unit = request.POST['unit']
            cartProduct = Products.objects.get(id = productId)
            if ShoppingCart.objects.filter(user = request.user, product = cartProduct, isPaid = False).exists():
                cart = ShoppingCart.objects.get(user = request.user, product = cartProduct, isPaid = False)
                cart.unit += int(unit)
                cart.save()
            else:
                cart = ShoppingCart.objects.create(
                    user = request.user,
                    product = cartProduct,
                    unit = unit,
                    total = cartProduct.price * int(unit),
                    isPaid = False
                )
                cart.save()
            return redirect('cart') 
        else:
            messages.warning(request, 'Lütfen Giriş Yapınız')
            return redirect('customerLogin')
    context = {
        'category': category,
        'product': product,
    }
    return render(request, 'product_detail.html', context)

def search(request):
    search_value = request.GET.get('search')
    if not search_value:
        messages.warning(request, 'Arama değeri bulunamadı.')
        return redirect('search')
    products = Products.objects.filter(name__icontains=search_value)
    if request.method == 'POST':
        if request.user.is_authenticated:
            productId = request.POST['productId']
            unit = request.POST['unit']
            cartProduct = Products.objects.get(id=productId)
            if ShoppingCart.objects.filter(user=request.user, product=cartProduct, isPaid=False).exists():
                cart = ShoppingCart.objects.get(user=request.user, product=cartProduct, isPaid=False)
                cart.unit += int(unit)
                cart.save()
            else:
                cart = ShoppingCart.objects.create(
                    user=request.user,
                    product=cartProduct,
                    unit=unit,
                    total=cartProduct.price * int(unit),
                    isPaid=False
                )
                cart.save()
            # Redirect to a different URL after adding the item to the cart
            return redirect('cart')
        else:
            messages.warning(request, 'Lütfen Giriş Yapınız')
            return redirect('customerLogin')

    context = {
        'products': products,
        'search_value': search_value,
    }
    return render(request, 'products.html', context)



def cart(request):
    orders = ShoppingCart.objects.filter(user = request.user, isPaid = False)
    cartTotal = 0
    for i in orders:
        cartTotal += i.total
    if request.method == 'POST':
        if 'pay' not in request.POST:
            orderId = request.POST['orderId']
            order = ShoppingCart.objects.get(id  = orderId)
        if 'delete' in request.POST:
            order.delete()
            messages.success(request, 'Ürün Silindi')
            return redirect('cart')
        elif 'update' in request.POST:
            unit = request.POST['unit']
            if unit == '0':
                order.delete()
            else:
                order.unit = unit
                order.save()
                messages.success(request, 'Ürün Güncellendi')
                return redirect('cart')
        elif 'pay' in request.POST:
            if Payment.objects.filter(user = request.user, isCompleted = False).exists():
                pass
            else:
                payment = Payment.objects.create(
                    user = request.user,
                    total = cartTotal,
                )
                payment.products.add(*orders)
                payment.save()
            return redirect('payment')
    context = {
        'orders' : orders,
        'cartTotal' : cartTotal
    }
    return render(request, 'shopping-cart.html', context)

