from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields=['name','slug']
    prepopulated_fields={'slug':('name',)}

admin.site.register(Products)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Payment)