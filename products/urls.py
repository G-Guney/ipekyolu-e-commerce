from django.urls import path
from .views import *

urlpatterns = [
    path('products-list/', products, name="products-list"),
    path('<str:category_slug>', products_by_category, name='products_by_category'),
    path('detail/<int:product_id>/<str:category_slug>/', product_detail, name='product_detail'),
    path('categories/', categories, name='categories'),
    path('search/', search, name='search'),
    path('cart/', cart, name='cart'),
    path('payment/', payment, name='payment'),
    path('result/', result, name='result'),
    path('success/', success, name='success'),
    path('failure/', fail, name='failure'),
]