from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price', 'status','video']

class DummyDataForm(forms.Form):
    category_count = forms.IntegerField(label='Number of Categories')
    num_products = forms.IntegerField(label='Number of Products', min_value=1, initial=1000)