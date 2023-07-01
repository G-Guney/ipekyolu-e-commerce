from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=50, unique=True, null=True,blank=True)
    title= models.CharField(max_length=50, null=True)
    image= models.ImageField(upload_to='categories', null=True, blank=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Products(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=45, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,blank=True)
    price = models.IntegerField(null=True)
    description = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if self.category and not self.category.slug:
            self.category.slug = slugify(self.category.name)
            self.category.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ShoppingCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    unit = models.IntegerField()
    total = models.IntegerField()
    isPaid = models.BooleanField()

    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        self.total = self.product.price * int(self.unit)
        super(ShoppingCart, self).save(*args, **kwargs)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(ShoppingCart)
    total = models.IntegerField()
    isCompleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


