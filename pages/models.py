from django.db import models
from django.views.generic import TemplateView
from products.models import ShoppingCart

# Create your models here.

class SiteCarousel(models.Model):
    head = models.CharField(max_length=100)
    title = models.TextField(max_length=500)
    image = models.ImageField(upload_to='carousels/')

    def __str__(self):
        return 'Başlık :  ' + self.head
    