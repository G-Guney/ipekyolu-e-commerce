from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

    
class SellerRegisterForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'company_name',]

    def __init__(self, *args, **kwargs):
        super(SellerRegisterForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        seller_group = Group.objects.get(name='Seller')
        seller_group.user_set.add(user)
        return user
    
class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]

    def __init__(self, *args, **kwargs):
        super(CustomerRegisterForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        customer_group = Group.objects.get(name='Customer')
        customer_group.user_set.add(user)
        return user