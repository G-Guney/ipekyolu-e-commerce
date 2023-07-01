from django.shortcuts import render, redirect
from products.models import Category
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
    carousels = SiteCarousel.objects.all()
    categories = Category.objects.all()[:4]
    context = {
        "carousels": carousels,
        'categories' : categories
    }
    return render(request, 'index.html', context)

def view_404(request, exception):
    messages.error(request, 'Geçersiz Adres! Anasayfaya yönlendirildiniz.')
    return redirect('/')

def view_500(request):
    messages.error(request, 'Sayfa Bulunamadı ! Anasayfaya yönlendirildiniz.')
    return redirect('/')