from django.forms import ModelForm
from .models import *

class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'image', 'title', 'description', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)    
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})