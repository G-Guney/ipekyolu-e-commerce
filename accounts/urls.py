from django.urls import path
from .views import *

urlpatterns = [
    path('sellerRegister/', sellerRegisterUser, name='sellerRegister'),
    path('sellerLogin/', sellerLoginUser, name='sellerLogin'),
    path('customerLogout/', customerLogout, name='customerLogout'),
    path('customerPanel/', customerPanel, name='customerPanel'),
    path('myOrders/', myOrders, name='orders'),
    path('customerRegister/', customerRegisterUser, name='customerRegister'),
    path('customerLogin/', customerLoginUser, name='customerLogin'),
    path('sellerPanel/', sellerPanel, name='sellerPanel'),
    path('sellerPanel/addProduct', addProduct, name='addProduct'),
    path('sellerPanel/myProducts', myProducts, name='myProducts'),
    path('sellerPanel/sellerLogout', sellerLogout, name='sellerLogout'),
]